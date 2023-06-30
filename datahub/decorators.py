from rest_framework_simplejwt.settings import api_settings
from django.http import JsonResponse
from functools import wraps
import json
import jwt
from rest_framework.exceptions import AuthenticationFailed, ParseError

from datahub.pipelines.hub import ApiResponse, Generic_Reference, fetch
from users.authentification import verify_jwt

def jwt_role_required(view_func):
  @wraps(view_func)
  def _wrapped_view(request, *args, **kwargs):
    req = json.loads(request.body)
    token = req.get('jwt')
    try:
      payload = verify_jwt(token)
      user = fetch(Generic_Reference(username=payload.username))
      request.user = user  # Now the role is available as request.user.role
      return view_func(request, *args, **kwargs)
    except AuthenticationFailed:
      return ApiResponse(401, "Authentification failed, user is not allowed to perform this action", None).json_response()
    except ParseError:
      return ApiResponse(400, "Invalid JWT token, token is required to perform actions", None).json_response()
  return _wrapped_view
