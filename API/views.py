import json
from django.middleware.csrf import get_token
from django.http import JsonResponse
from rest_framework_jwt.settings import api_settings
from cas import CASClient

import API.datapipeline.PipelineHub as pipe
from API.datapipeline.PipelineHub import ApiRequest
from API.decorators import jwt_role_required
import sussy_crudproject.settings as settings
import API.datapipeline.PipelineHub as pipe
from API.datapipeline.PipelineHub import ReferenceData

def csrfToken(request):
  return JsonResponse({'csrfToken': get_token(request)})


def authenticate(request):
  ticket = request.GET.get('ticket')
  service = request.build_absolute_uri()
  service = 'http://localhost:8000/api/auth/'
  client = CASClient(server_url=settings.CAS_SERVER_URL, service_url=service, version=3)
  username, attributes, pgtiou = client.verify_ticket(ticket)

  if not username:
    return JsonResponse({"error": "Invalid ticket"}, status=400)

  # User is authenticated, issue JWT
  pipe.fetch()
  user = Student.objects.get(username=username)
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
    reference = ReferenceData(req.data.get('reference'))
    
    if action == 'create':
      if check_permission_create(reference, req.jwt):
        return pipe.insert(reference)
      return JsonResponse({"error": "User not allowed"}, status=403)

    elif action == 'update':
      if check_permission_update(reference, req.jwt):
        return pipe.update(reference)
      return JsonResponse({"error": "User not allowed"}, status=403)

    elif action == 'fetch_all':
      if check_permission_read(reference, req.jwt):
        return pipe.fetch_all(reference)
      return JsonResponse({"error": "User not allowed"}, status=403)
      
    elif action == 'fetch':
      if check_permission_read(reference, req.jwt):
        return pipe.fetch(reference)
      return JsonResponse({"error": "User not allowed"}, status=403)
    
    elif action == 'remove':
      if check_permission_delete(reference, req.jwt):
        return pipe.delete(reference)
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