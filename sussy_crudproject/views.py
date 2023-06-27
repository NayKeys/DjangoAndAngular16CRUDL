from django.http import HttpResponse
from django.template import loader
from . import settings

def index(request):
  template = loader.get_template('index.html')
  context = {
    'cas_url': settings.CAS_SERVER_URL,
  }
  return HttpResponse(template.render(context, request))