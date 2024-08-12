from django.template.response import TemplateResponse
from datetime import datetime, timedelta
import locale
import requests


# Create your views here.
def repertoire(request):
    template = "repertoire/repertoire.html"
    locale.setlocale(locale.LC_TIME, "pl_PL.utf-8")
    start_day = datetime.now()
    sever_days_forward = {}
    for day in range(1, 8):
        start_day = start_day + timedelta(days=1)
        sever_days_forward[start_day.strftime("%Y-%m-%d")] = start_day.strftime("%A")
    sever_days = {"days": sever_days_forward}
    day = request.GET.get("date")
    return TemplateResponse(request, template, sever_days)
