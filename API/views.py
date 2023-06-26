import json
from django.http import JsonResponse
import API.datapipeline.PipelineHub as pipe
from API.datapipeline.PipelineHub import ApiRequest

from django.middleware.csrf import get_token
from django.http import JsonResponse

def csrfToken(request):
  return JsonResponse({'csrfToken': get_token(request)})

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
        return pipe.update(req.data.get('reference'))
      return JsonResponse({"error": "User not allowed"}, status=403)

    elif action == 'fetch_all':
      if check_permission_read(req.data.get('reference'), req.jwt):
        return pipe.fetch_all(req.data.get('reference'))
      return JsonResponse({"error": "User not allowed"}, status=403)
      
    elif action == 'fetch':
      if check_permission_read(req.data.get('reference'), req.jwt):
        return pipe.fetch(req.data.get('reference'))
      return JsonResponse({"error": "User not allowed"}, status=403)
    
    elif action == 'delete':
      if check_permission_delete(req.data.get('reference'), req.jwt):
        return pipe.delete(req.data.get('reference'))
      return JsonResponse({"error": "User not allowed"}, status=403)
    
    else:
      return JsonResponse({"error": "Invalid method"}, status=400)

def check_permission_create(data, jwt):
  return True
def check_permission_update(data, jwt):
  return True
def check_permission_read(data, jwt):
  return True
def check_permission_delete(data, jwt):
  return True