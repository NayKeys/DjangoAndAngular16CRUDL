import json
from django.middleware.csrf import get_token
from django.http import JsonResponse
from rest_framework_simplejwt.settings import api_settings
from cas import CASClient
from rest_framework.exceptions import AuthenticationFailed, ParseError

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
from API.datapipeline.PipelineHub import check_permission_create, check_permission_update, check_permission_delete, check_permission_fetch, check_permission_fetch_all

"""NOTE:
  actions shouldnt implement a try catch block, that block should be specific to each different data pipelines
"""

def csrfToken(request):
  return JsonResponse({'csrfToken': get_token(request)})

def cas_validation(request):
  req = json.loads(request.body)
  ticket = req.get('ticket')
  service = request.build_absolute_uri()
  service = 'http://localhost:8000/api/cas/'
  client = CASClient(server_url=settings.CAS_SERVER_URL, service_url=service, version=3)
  username, attributes, pgtiou = client.verify_ticket(ticket)
  if not username:
    username = 'yanregoj64'
    # return JsonResponse({"error": "Invalid ticket"}, status=400)
  # User is authenticated, issue JWT
  reference = pipe.fetch(ReferenceData(username=username))
  if reference is None:
    return ApiResponse(401, "Authentification failed", None)
  else:
    token = create_jwt(username, reference.reference.role)
    response = JsonResponse({"status": 200, "jwt": token}, status=200)
    return response

def authenticate(request):
  req = json.loads(request.body)
  token = req.get('jwt')
  try:
    payload = verify_jwt(token)
  except AuthenticationFailed:
    return ApiResponse(401, "Authentification failed", None).JsonResponse()
  except ParseError:
    return ApiResponse(400, "Invalid JWT token", None).JsonResponse()
  return ApiResponse(200, "Authentification success!", None).JsonResponse()

@jwt_role_required  # AMAZING PYTHON FEATURE
def execute(request):
  if request.method == 'POST':
    req: ApiRequest = ApiRequest(json.loads(request.body))
    action = req.action
    reference = ReferenceData.fromDict(req.data)
    
    if action == 'create':
      try:
        if check_permission_create(reference, request.user):
          action_performed = pipe.insert(reference)
          if (action_performed ):
            return ApiResponse(200, "Succesfuly created element with", [ReferenceData.fromDict(fetched_data)]).JsonResponse()
        else:
          return ApiResponse(403, "Error: User is not allowed to perform this action", None).JsonResponse()
      except Exception as e:
        e.print_exc()
        return ApiResponse(500, "Could not create element\n error-message: "+str(e), None).JsonResponse()

    elif action == 'update':
      try:
        if check_permission_update(reference, request.user):
          action_performed = pipe.update(reference)
          if (action_performed):
            return ApiResponse(200, "Succesfuly updated element with id = "+str(reference.id), None).JsonResponse()
        else:
          return ApiResponse(403, "Error: User is not allowed to perform this action", None).JsonResponse()
      except Exception as e:
        e.print_exc()
        return ApiResponse(500, "Could not update element with id = "+str(reference.id)+"\n error-message: "+str(e), None).JsonResponse()
    
    elif action == 'fetch_all':
      try:
        if check_permission_fetch_all(reference, request.user):
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
        if check_permission_fetch(reference, request.user):
          fetched_data = pipe.fetch(reference)
          if (not fetched_data is None):
            return ApiResponse(200, "Succesfuly retrieved element with id = "+str(reference.id), fetched_data).JsonResponse()
        else:
          return ApiResponse(403, "Error: User is not allowed to perform this action", fetched_data).JsonResponse()
      except Exception as e:
        e.print_exc()
        return ApiResponse(404, "No data found with this query id = "+reference.id+"\n error-message: "+str(e), None).JsonResponse()
    
    elif action == 'remove':
      try:
        if check_permission_delete(reference, request.user):
          action_performed = pipe.delete(reference)
          if (action_performed):
            return ApiResponse(200, "Succesfuly retrieved element with id = "+str(reference.id), None).JsonResponse()
        else:
          return ApiResponse(403, "Error: User is not allowed to perform this action", None).JsonResponse()
      except Exception as e:
        e.print_exc()
        return ApiResponse(500, "Could not delete element with id = "+reference.id+"\n error-message: "+str(e), None).JsonResponse()
    else:
      return JsonResponse({"error": "Invalid method"}, status=400)