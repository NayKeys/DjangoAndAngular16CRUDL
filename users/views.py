from django.shortcuts import render

# Create your views here.
import json
import sys
from django.middleware.csrf import get_token
from django.http import JsonResponse
from cas import CASClient
from rest_framework.exceptions import AuthenticationFailed, ParseError
import logging


from users.models import Profile
import datahub.pipelines.hub as pipe
import sussy_crudproject.settings as settings
from datahub.pipelines.hub import ApiResponse
from users.authentification import verify_jwt
from users.authentification import create_jwt
import sussy_crudproject.settings as settings
from users.decorators import jwt_role_required 

"""NOTE:
  actions shouldnt implement a try catch block, that block should be specific to each different data pipelines
"""

"""_summary_
"""
@jwt_role_required
def permissions(request):
  user_info = {
    "username": request.user.username,
    "role": request.user.role,
    "can_create": request.user.can_read,
    "can_read": request.user.can_read,
    "can_update": request.user.can_update,
    "can_delete": request.user.can_delete,
  }
  return JsonResponse({"permissions": user_info})

"""_summary_
@params request: django request object containing a cas ticket
@description API route api/cas/ that validates cas ticket and create a custom rest-framework jwt
@returns a Django response following ./restapiresponse.json pattern including a  jwt token if the user is authenticated
"""
def cas_validation(request):
  logger = logging.getLogger(__name__)
  body = json.loads(request.body)
  ticket = body.get('ticket')
  service = request.build_absolute_uri()[:-len(settings.CAS_ENDPOINT)]
  logger.info(service+"\n")
  if request.is_secure():
    service = service.replace("http://", "https://")
  client = CASClient(server_url=settings.CAS_SERVER_URL, service_url=service, version=3)
  username, attributes, pgtiou = client.verify_ticket(ticket)
  if not username:
    return JsonResponse({"error": "Invalid ticket"}, status=400)
  # User is authenticated, issue JWT
  user = Profile.objects.get(username=username)
  if user is None:
    return ApiResponse(401, "Authentification failed", None)
  else:
    token = create_jwt(username, user.role)
    response = JsonResponse({"status": 200, "token": token}, status=200)
    return response

"""_summary_
@params request: django request object containting a jwt token
@description API route api/auth/ that validates jwt token
@returns a django response following ./restapiresponse.json with status 200 if the token is valid, 401 if not
"""
def authenticate(request):
  headers = request.headers
  token = headers.get('token')
  try:
    payload = verify_jwt(token)
  except AuthenticationFailed:
    return ApiResponse(401, "Authentification failed", None).json_response()
  except ParseError:
    return ApiResponse(400, "Invalid JWT token", None).json_response()
  return ApiResponse(200, "Authentification success!", None).json_response()