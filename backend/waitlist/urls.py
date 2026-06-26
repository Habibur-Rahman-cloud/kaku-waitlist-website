from django.urls import path
from . import views

urlpatterns = [
    # APIs
    path('waitlist/join/', views.join_waitlist, name='api_join_waitlist'),
    path('waitlist/count/', views.get_waitlist_count, name='api_waitlist_count'),
    
    # Dashboard Actions (Protected by login_required in views)
    path('dashboard/', views.dashboard_home, name='dashboard_home'),
    path('dashboard/delete/<int:user_id>/', views.delete_user, name='dashboard_delete_user'),
    path('dashboard/export/', views.export_csv, name='dashboard_export_csv'),
    path('dashboard/broadcast/', views.send_broadcast, name='dashboard_broadcast'),
]
