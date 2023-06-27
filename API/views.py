import json
import API.datapipeline.PipelineHub as pipe
from API.datapipeline.PipelineHub import ApiRequest

from django.middleware.csrf import get_token
from django.http import JsonResponse
from django_cas_ng.views import _service_url, _verify
from rest_framework_jwt.settings import api_settings

from decorators import jwt_role_required
from models import Student

def csrfToken(request):
  return JsonResponse({'csrfToken': get_token(request)})


def authenticate(request):
  ticket = request.GET.get('ticket')
  service = _service_url(request)
  id, attributes, pgtiou = _verify(ticket, service)

  if not id:
      return JsonResponse({"error": "Invalid ticket"}, status=400)

  # User is authenticated, issue JWT
  user = Student.objects.get(id=id)
  jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
  jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
  payload = jwt_payload_handler(user)
  
  # Add 'role' to JWT payload
  payload['role'] = user.role  # Assuming 'role' is stored in 'user.role'
  jwt_token = jwt_encode_handler(payload)
  response = JsonResponse({"token": jwt_token})

  # Set JWT as a cookie, with a max age of 14 hours
  max_age = 14 * 60 * 60
  response.set_cookie('jwt', jwt_token, max_age=max_age, httponly=True)
  return response

@jwt_role_required  # AMAZING PYTHON FEATURE
def execute(request):
  if request.method == 'POST':
    req: ApiRequest = ApiRequest(json.loads(request.body))
    action = req.action
    
    if action == 'create':
      if check_permission_create(req.data.get('reference'), req.jwt):
        return pipe.insert(req.data.get('reference'))
      return JsonResponse({"error": "User not allowed"}, status=403)

    elif action == 'update':
      if check_permission_update(req.data.get('reference'), req.jwt):
        return pipe.update(req.data.get('id'), req.data.get('reference'))
      return JsonResponse({"error": "User not allowed"}, status=403)

    elif action == 'fetch_all':
      if check_permission_read(req.data.get('reference'), req.jwt):
        return pipe.fetch_all(req.data.get('reference'))
      return JsonResponse({"error": "User not allowed"}, status=403)
      
    elif action == 'fetch':
      if check_permission_read(req.data.get('reference'), req.jwt):
        return pipe.fetch(req.data.get('id'), req.data.get('reference'))
      return JsonResponse({"error": "User not allowed"}, status=403)
    
    elif action == 'remove':
      if check_permission_delete(req.data.get('reference'), req.jwt):
        return pipe.delete(req.data.get('id'), req.data.get('reference'))
      return JsonResponse({"error": "User not allowed"}, status=403)
    
    else:
      return JsonResponse({"error": "Invalid method"}, status=400)

from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model

def validate_cas_ticket(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    ticket = data.get('ticket')
    
    # Replace this with the actual validation endpoint
    casValidateUrl = 'https://cas.ensea.fr/validate'

    params = {
        'service': 'http://your-application-url.com',  # the URL of your application
        'ticket': ticket
    }
    response = requests.get(casValidateUrl, params=params)
    
    if response.status_code == 200:
      # CAS server will respond with 'yes' on success and 'no' on failure
      if response.text.split()[0] == 'yes':
        username = response.text.split()[1]
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist"}, status=400)

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return JsonResponse({"token": token})

  return JsonResponse({"error": "Invalid request"}, status=400)

def check_permission_create(data, jwt):
  return True
def check_permission_update(data, jwt):
  return True
def check_permission_read(data, jwt):
  return True
def check_permission_delete(data, jwt):
  return True