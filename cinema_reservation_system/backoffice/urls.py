from . import views
from django.urls import path


urlpatterns = [
    path("", views.index, name="index"),
    path("pdf_report/", views.pdf_report, name="pdf_report"),
    path("html_report/", views.html_report, name="html_report"),

]
