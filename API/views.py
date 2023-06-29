import json
from django.middleware.csrf import get_token
from django.http import JsonResponse
from rest_framework_simplejwt.settings import api_settings
from cas import CASClient

import API.datapipeline.PipelineHub as pipe
from API.datapipeline.PipelineHub import ApiRequest
from API.decorators import jwt_role_required
import sussy_crudproject.settings as settings
import API.datapipeline.PipelineHub as pipe
from API.datapipeline.PipelineHub import ReferenceData
from API.datapipeline.PipelineHub import ApiResponse
from API.authentification import verify_jwt
from API.authentification import create_jwt
import sussy_crudproject.settings as settings

"""NOTE:
  actions shouldnt implement a try catch block, that block should be specific to each different data pipelines
"""

def csrfToken(request):
  return JsonResponse({'csrfToken': get_token(request)})

def cas_validation(request):
  req = json.loads(request.body)
  ticket = req.get('ticket')
  service = request.build_absolute_uri()
  service = 'http://localhost:8000/api/auth/'
  client = CASClient(server_url=settings.CAS_SERVER_URL, service_url=service, version=3)
  username, attributes, pgtiou = client.verify_ticket(ticket)
  if not username:
    return JsonResponse({"error": "Invalid ticket"}, status=400)
  # User is authenticated, issue JWT
  reference = pipe.fetch(ReferenceData(username=username))
  if reference is None:
    return ApiResponse(401, "Authentification failed", None)
  else:
    reference = ReferenceData.fromDict(reference)
    token = create_jwt(username, reference.reference.role)
    response = JsonResponse({"jwt": token})
    # Set JWT as a cookie, with a max age of 14 hours
    max_age = settings.TOKEN_LIFETIME_HOURS * 60 * 60
    response.set_cookie('jwt', token, max_age=max_age, httponly=True)
    return response

def authenticate(request):
  req = json.loads(request.body)
  token = req.get('jwt')
  verif = verify_jwt(token)
  return True

# @jwt_role_required  # AMAZING PYTHON FEATURE
def execute(request):
  if request.method == 'POST':
    req: ApiRequest = ApiRequest(json.loads(request.body))
    action = req.action
    reference = ReferenceData.fromDict(req.data)
    
    if action == 'create':
      try:
        if check_permission_create(reference, req.jwt):
          action_performed = pipe.insert(reference)
          if (action_performed ):
            return ApiResponse(200, "Succesfuly retrieved element with id = "+str(id), [ReferenceData.fromDict(fetched_data)]).JsonResponse()
        else:
          return ApiResponse(403, "Error: User is not allowed to perform this action", None).JsonResponse()
      except Exception as e:
        e.print_exc()
        return ApiResponse(500, "Could not create element\n error-message: "+str(e), None).JsonResponse()

    elif action == 'update':
      try:
        if check_permission_update(reference, req.jwt):
          action_performed = pipe.update(reference)
          if (action_performed):
            return ApiResponse(200, "Succesfuly updated element with id = "+reference.id, None).JsonResponse()
        else:
          return ApiResponse(403, "Error: User is not allowed to perform this action", None).JsonResponse()
      except Exception as e:
        e.print_exc()
        return ApiResponse(500, "Could not update element with id = "+reference.id+"\n error-message: "+str(e), None).JsonResponse()
    
    elif action == 'fetch_all':
      try:
        if check_permission_read(reference, req.jwt):
          fetched_data = pipe.fetch_all(reference)
          if (not fetched_data is None):
            return ApiResponse(200, "Succesfuly retrieved elements", fetched_data).JsonResponse()
        else:
          return ApiResponse(403, "Error: User is not allowed to perform this action", fetched_data).JsonResponse()
      except Exception as e:
        e.print_exc()
        return ApiResponse(404, "No data found with this query role = "+reference.role+"\n error-message: "+str(e), None).JsonResponse()
    
    elif action == 'fetch':
      try:
        if check_permission_read(reference, req.jwt):
          fetched_data = pipe.fetch(reference)
          if (not fetched_data is None):
            return ApiResponse(200, "Succesfuly retrieved element with id = "+str(id), fetched_data).JsonResponse()
        else:
          return ApiResponse(403, "Error: User is not allowed to perform this action", fetched_data).JsonResponse()
      except Exception as e:
        e.print_exc()
        return ApiResponse(404, "No data found with this query id = "+reference.id+"\n error-message: "+str(e), None).JsonResponse()
    
    elif action == 'remove':
      try:
        if check_permission_delete(reference, req.jwt):
          action_performed = pipe.delete(reference)
          if (action_performed):
            return ApiResponse(200, "Succesfuly retrieved element with id = "+str(id), None).JsonResponse()
        else:
          return ApiResponse(403, "Error: User is not allowed to perform this action", None).JsonResponse()
      except Exception as e:
        e.print_exc()
        return ApiResponse(500, "Could not delete element with id = "+reference.id+"\n error-message: "+str(e), None).JsonResponse()
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