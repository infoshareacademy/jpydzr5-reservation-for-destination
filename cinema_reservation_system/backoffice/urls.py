from . import views
from django.urls import path

app_name = 'backoffice'

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("report/", views.report, name="report"),
    path("charts/", views.charts, name="charts"),
    path("user_panel/", views.user_panel, name="user_panel"),
]
