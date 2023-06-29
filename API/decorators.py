from rest_framework_simplejwt.settings import api_settings
from django.http import JsonResponse
from functools import wraps
import json
import jwt
from API.authentification import verify_jwt
from rest_framework.exceptions import AuthenticationFailed, ParseError

def jwt_role_required(view_func):
  @wraps(view_func)
  def _wrapped_view(request, *args, **kwargs):
    req = json.loads(request.body)
    token = req.get('jwt')
    try:
      verif = verify_jwt(token)
    except AuthenticationFailed:
      return ApiResponse(401, "Authentification failed", None)
    except ParseError:
      return ApiResponse(400, "Invalid JWT token", None)
    return ApiResponse(200, "Authentification success!", None)
    if not jwt_token:
      return JsonResponse({"error": "No JWT token provided"}, status=401)

    try:
        payload = jwt_decode_handler(jwt_token)
    except:
        return JsonResponse({"error": "Invalid JWT token"}, status=401)

    request.role = payload.get('role')  # Now the role is available as request.role

    return view_func(request, *args, **kwargs)
  return _wrapped_view
