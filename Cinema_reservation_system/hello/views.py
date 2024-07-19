from django.template.response import TemplateResponse


def index(request):
    template = "hello/hello.html"
    ctx = {
        "name1": "Inga",
        "name2": "Przemek"
    }
    return TemplateResponse(request, template, ctx)
