from django.http import HttpResponse
from django.template import loader

from flags import FLAGS

def shadow(request):
    context = {"flag": FLAGS["dir_traveler"][0]}
    template = loader.get_template('traveler/shadow.html')
    return HttpResponse(template.render(context, request))

def passwd(request):
    context = {"flag": FLAGS["dir_traveler"][0]}
    template = loader.get_template('traveler/passwd.html')
    return HttpResponse(template.render(context, request))
