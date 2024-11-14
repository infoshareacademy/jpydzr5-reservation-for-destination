from . import views
from django.urls import path

app_name = 'backoffice'

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("report/", views.report, name="report"),
    path("charts/", views.charts, name="charts"),
    path("user_panel/", views.user_panel, name="user_panel"),
    path('qr_code/<int:reservation_id>/', views.qr_code_view, name='qr_code'),
    path('validate_ticket/<str:uuid>/', views.validate_ticket, name='validate_ticket'),
    path('validate_ticket/', views.validate_ticket, name='validate_ticket_home'),
]
