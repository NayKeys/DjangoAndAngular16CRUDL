import json
from django.http import JsonResponse
import DataPipeline as pipe
from DataPipeline import ApiRequest

def execute(request):
  if request.method == 'POST':
    data: ApiRequest = ApiRequest(json.loads(request.body))
    action = data.action
    
    if action == 'insert':
      if check_permission_create(data.reference, data.get('jwt')):
        return pipe.insert(data.reference)
      return JsonResponse({"error": "User not allowed"}, status=403)

    elif action == 'insert_all':  # TO BE DELETED
      if check_permission_create(data.reference, data.get('jwt')):
        dataset = data.reference
        return pipe.insert_all(dataset)
      return JsonResponse({"error": "User not allowed"}, status=403)

    elif action == 'update':
      if check_permission_update(data.reference, data.get('jwt')):
        return pipe.update(data.reference)
      return JsonResponse({"error": "User not allowed"}, status=403)

    elif action == 'fetch_all':
      if check_permission_read(data.reference, data.get('jwt')):
        return pipe.fetch_all(data.reference)
      return JsonResponse({"error": "User not allowed"}, status=403)
      
    elif action == 'fetch':
      if check_permission_read(data.reference, data.get('jwt')):
        return pipe.fetch(data.reference)
      return JsonResponse({"error": "User not allowed"}, status=403)
    
    elif action == 'delete':
      if check_permission_delete(data.reference, data.get('jwt')):
        return pipe.delete(data.reference)
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