import json
from django.http import JsonResponse
import DataPipeline as pipe

def execute(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    action = data.get('action')
    
  if action == 'insert':
    if check_permission_create(data.get('student'), data.get('jwt')):
      data = data.get('student')
      return pipe.insert(data)
    return JsonResponse({"error": "User not allowed"}, status=403)

  elif action == 'insert_all':
    if check_permission_create(data.get('student'), data.get('jwt')):
      dataset = data.get('student')
      return pipe.insert_all(dataset)
    return JsonResponse({"error": "User not allowed"}, status=403)

  elif action == 'update':
    if check_permission_update(data.get('student'), data.get('jwt')):
      id = data.get('id')
      data = data.get('student')
    return JsonResponse({"error": "User not allowed"}, status=403)
    return pipe.update(id, data)

  elif action == 'fetch_all':
    if check_permission_read(data.get('student'), data.get('jwt')):
      field = data.get('field')
      return pipe.fetch_all(field)
    return JsonResponse({"error": "User not allowed"}, status=403)
    
  elif action == 'fetch':
    if check_permission_read(data.get('student'), data.get('jwt')):
      id = data.get('id')
      return pipe.fetch(id)
    return JsonResponse({"error": "User not allowed"}, status=403)
  
  elif action == 'delete':
    if check_permission_delete(data.get('student'), data.get('jwt')):
      id = data.get('id')
      return pipe.delete(id)
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