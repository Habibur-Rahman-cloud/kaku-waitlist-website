import csv
import datetime
import logging
import threading
import time
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.utils import timezone
from .models import WaitlistUser
from .serializers import WaitlistUserSerializer
from .services import EmailService

logger = logging.getLogger(__name__)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def send_welcome_email_task(user_id):
    try:
        user = WaitlistUser.objects.get(pk=user_id)
        if EmailService.send_welcome_email(user.email):
            user.welcome_email_sent = True
            user.last_email_sent = timezone.now()
            user.save(update_fields=['welcome_email_sent', 'last_email_sent'])
    except WaitlistUser.DoesNotExist:
        pass

def send_broadcast_task(subject, body, recipients):
    """Sends emails in batches of 50 with a 2-second delay to avoid SMTP rate limits."""
    batch_size = 50
    delay = 2.0
    
    for i in range(0, len(recipients), batch_size):
        batch = recipients[i:i + batch_size]
        success_count = EmailService.send_broadcast_email(subject, body, batch)
        
        if success_count > 0:
            now = timezone.now()
            WaitlistUser.objects.filter(email__in=batch).update(last_email_sent=now)
            
        if i + batch_size < len(recipients):
            time.sleep(delay)

# --- API VIEWS ---

@api_view(['POST'])
@permission_classes([AllowAny])
def join_waitlist(request):
    honeypot = request.data.get('honeypot', '')
    if honeypot:
        ip = get_client_ip(request)
        logger.warning(f"Honeypot triggered from IP: {ip}. Value: {honeypot}")
        # Silently reject bots but return success
        return Response({"message": "Successfully joined waitlist."}, status=status.HTTP_201_CREATED)

    serializer = WaitlistUserSerializer(data=request.data)
    if serializer.is_valid():
        try:
            # Capture IP and User Agent
            ip_address = get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')

            user = serializer.save(ip_address=ip_address, user_agent=user_agent)
            
            # Send welcome email in background
            thread = threading.Thread(target=send_welcome_email_task, args=(user.id,))
            thread.start()

            return Response({"message": "Successfully joined waitlist."}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"message": "You are already on the waitlist!"}, status=status.HTTP_409_CONFLICT)
    
    if 'email' in serializer.errors and getattr(serializer.errors['email'][0], 'code', '') == 'unique':
        return Response({"message": "You are already on the waitlist!"}, status=status.HTTP_409_CONFLICT)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_waitlist_count(request):
    count = WaitlistUser.objects.count()
    return Response({"count": count})


# --- DASHBOARD VIEWS ---

@login_required(login_url='/dashboard/login/')
def dashboard_home(request):
    query = request.GET.get('q', '')
    if query:
        entries = WaitlistUser.objects.filter(email__icontains=query)
    else:
        entries = WaitlistUser.objects.all()
    
    # Analytics
    total_users = WaitlistUser.objects.count()
    
    now = timezone.now()
    today = now.date()
    yesterday = today - datetime.timedelta(days=1)
    
    today_joins = WaitlistUser.objects.filter(joined_at__date=today).count()
    yesterday_joins = WaitlistUser.objects.filter(joined_at__date=yesterday).count()
    
    week_ago = now - datetime.timedelta(days=7)
    weekly_joins = WaitlistUser.objects.filter(joined_at__gte=week_ago).count()
    
    month_ago = now - datetime.timedelta(days=30)
    monthly_joins = WaitlistUser.objects.filter(joined_at__gte=month_ago).count()
    
    last_signup = WaitlistUser.objects.first()
    
    welcome_sent = WaitlistUser.objects.filter(welcome_email_sent=True).count()
    welcome_failed = total_users - welcome_sent
    
    broadcast_sent = WaitlistUser.objects.filter(last_email_sent__isnull=False).count()
    
    # Top sources
    top_sources = list(WaitlistUser.objects.exclude(source__isnull=True).exclude(source='').values('source').annotate(count=Count('source')).order_by('-count')[:5])

    page_size = 20
    page = int(request.GET.get('page', 1))
    total_pages = (entries.count() // page_size) + (1 if entries.count() % page_size > 0 else 0)
    entries_page = entries[(page-1)*page_size:page*page_size]

    context = {
        'entries': entries_page,
        'total_users': total_users,
        'today_joins': today_joins,
        'yesterday_joins': yesterday_joins,
        'weekly_joins': weekly_joins,
        'monthly_joins': monthly_joins,
        'last_signup': last_signup,
        'welcome_sent': welcome_sent,
        'welcome_failed': welcome_failed,
        'broadcast_sent': broadcast_sent,
        'top_sources': top_sources,
        'query': query,
        'page': page,
        'total_pages': total_pages,
        'has_next': page < total_pages,
        'has_prev': page > 1,
    }
    return render(request, 'dashboard/home.html', context)

@login_required(login_url='/dashboard/login/')
def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(WaitlistUser, pk=user_id)
        user.delete()
        messages.success(request, f'User {user.email} deleted successfully.')
    return redirect('dashboard_home')

@login_required(login_url='/dashboard/login/')
def export_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="waitlist.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(['ID', 'Email', 'Source', 'IP Address', 'User Agent', 'Verified', 'Welcome Sent', 'Last Email', 'Joined At'])
    for u in WaitlistUser.objects.all().order_by('joined_at'):
        writer.writerow([u.id, u.email, u.source, u.ip_address, u.user_agent, u.verified, u.welcome_email_sent, u.last_email_sent, u.joined_at])
    return response

@login_required(login_url='/dashboard/login/')
def send_broadcast(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        recipient = request.POST.get('recipient')

        if not subject or not body:
            messages.error(request, "Subject and body are required.")
            return redirect('dashboard_home')

        if recipient == 'all':
            target_users = WaitlistUser.objects.all()
        else:
            target_users = WaitlistUser.objects.filter(email=recipient)

        recipients = [u.email for u in target_users]
        
        # Dispatch background thread for broadcast
        thread = threading.Thread(target=send_broadcast_task, args=(subject, body, recipients))
        thread.start()

        messages.success(request, f"Broadcast email dispatched to {len(recipients)} recipient(s) in the background.")
            
    return redirect('dashboard_home')
