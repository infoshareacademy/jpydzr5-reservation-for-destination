from django.template.response import TemplateResponse


# Create your views here.
def price_list(request):
    template = "price_list/price_list.html"
    message = {"message": "OK!"}
    return TemplateResponse(request, template, message)
