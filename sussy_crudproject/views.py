from django.http import HttpResponse, JsonResponse
from django.template import loader
from . import settings

def index(request):
  template = loader.get_template('index.html')
  context = {
    'cas_url': settings.CAS_SERVER_URL,
    'token_lifetime_hours': settings.TOKEN_LIFETIME_HOURS,
  }
  return HttpResponse(template.render(context, request))

def health(request):
  return JsonResponse({'status': ':D'}, status=200)