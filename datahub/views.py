import json
from django.http import JsonResponse

import datahub.pipelines.hub as pipe
from datahub.pipelines.hub import ApiRequest
from datahub.decorators import jwt_role_required
import datahub.pipelines.hub as pipe
from datahub.pipelines.hub import ReferenceData
from datahub.pipelines.hub import ApiResponse
from datahub.pipelines.hub import check_permission_create, check_permission_update, check_permission_delete, check_permission_fetch, check_permission_fetch_all

# Create your views here.
"""_summary_
@params request: django request object whom body follows ./restapirequest.json pattern. The request should contain a jwt token and a non-empty reference
@description API route api/execute/ that performs the requested actions on the data bases
@returns a django response following ./restapiresponse.json pattern with or without data depending on the action performed
"""
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