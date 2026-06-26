from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from waitlist import views as waitlist_views

urlpatterns = [
    # APIs
    path('api/waitlist/join/', waitlist_views.join_waitlist, name='api_join_waitlist'),
    path('api/waitlist/count/', waitlist_views.get_waitlist_count, name='api_waitlist_count'),
    path('api/health/', waitlist_views.health_check, name='health_check'),
    
    # Default Admin
    path('admin/', admin.site.urls),
    
    # Custom Dashboard Auth
    path('dashboard/login/', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    path('dashboard/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Custom Dashboard Views
    path('dashboard/', waitlist_views.dashboard_home, name='dashboard_home'),
    path('dashboard/delete/<int:user_id>/', waitlist_views.delete_user, name='dashboard_delete_user'),
    path('dashboard/export/', waitlist_views.export_csv, name='dashboard_export_csv'),
    path('dashboard/broadcast/', waitlist_views.send_broadcast, name='dashboard_broadcast'),
]
