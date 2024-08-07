from django.template.response import TemplateResponse


# Create your views here.
def basket(request):
    template = "basket/basket.html"
    message = {"message": "OK!"}
    return TemplateResponse(request, template, message)
