from rest_framework_simplejwt.settings import api_settings
from django.http import JsonResponse
from functools import wraps
import json
import jwt
from rest_framework.exceptions import AuthenticationFailed, ParseError
from users.models import Profile

from datahub.pipelines.hub import ApiResponse, fetch
from users.authentification import verify_jwt

def jwt_role_required(view_func):
  @wraps(view_func)
  def _wrapped_view(request, *args, **kwargs):
    token = request.headers.get('token')
    try:
      payload = verify_jwt(token)
      user = Profile.objects.get(username=payload.username)
      request.user = user  # Now the role is available as request.user.role
      return view_func(request, *args, **kwargs)
    except AuthenticationFailed:
      return ApiResponse(401, "Authentification failed, user is not allowed to perform this action", None).json_response()
    except ParseError:
      return ApiResponse(400, "Invalid JWT token, token is required to perform actions", None).json_response()
  return _wrapped_view
