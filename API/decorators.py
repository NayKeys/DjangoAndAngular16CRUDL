from rest_framework_jwt.settings import api_settings
from django.http import JsonResponse
from functools import wraps

def jwt_role_required(view_func):
  @wraps(view_func)
  def _wrapped_view(request, *args, **kwargs):
    jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
    jwt_token = request.COOKIES.get('jwt')
    
    if not jwt_token:
        return JsonResponse({"error": "No JWT token provided"}, status=401)

    try:
        payload = jwt_decode_handler(jwt_token)
    except:
        return JsonResponse({"error": "Invalid JWT token"}, status=401)

    request.role = payload.get('role')  # Now the role is available as request.role

    return view_func(request, *args, **kwargs)
  return _wrapped_view
