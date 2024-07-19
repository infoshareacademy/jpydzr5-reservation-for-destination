from django.template.response import TemplateResponse


def index(request):
    template = "index/index.html"
    return TemplateResponse(request, template)