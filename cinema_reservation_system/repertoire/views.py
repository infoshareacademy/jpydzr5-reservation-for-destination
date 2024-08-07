from django.template.response import TemplateResponse


# Create your views here.
def repertoire(request):
    template = "repertoire/repertoire.html"
    message = {"message": "OK!"}
    return TemplateResponse(request, template, message)
