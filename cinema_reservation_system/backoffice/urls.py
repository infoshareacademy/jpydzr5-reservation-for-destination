from . import views
from django.urls import path

app_name = 'backoffice'

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("pdf_report/", views.pdf_report, name="pdf_report"),
    path("report/", views.report, name="report"),
    path("user_panel/", views.user_panel, name="user_panel"),
]
