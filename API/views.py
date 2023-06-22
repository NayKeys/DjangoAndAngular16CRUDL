import json
from django.http import JsonResponse
import DataPipeline as pipe

def execute(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        
        if action == 'insert':
            student = data.get('student')
            return pipe.insert(student)

        elif action == 'insert_all':
            students = data.get('students')
            return pipe.insert_all(students)

        elif action == 'update':
            id = data.get('id')
            student = data.get('student')
            return pipe.update(id, student)

        elif action == 'fetch_all':
            field = data.get('field')
            return pipe.fetch_all(field)
            
        elif action == 'fetch':
            id = data.get('id')
            return pipe.fetch(id)

    else:
        return JsonResponse({"error": "Invalid method"}, status=400)