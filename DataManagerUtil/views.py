from django.shortcuts import render
import petl as etl
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

from .models import Student

@csrf_exempt
def execute(request):
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)
  action = body.get('action')
  print('api/execute : executing', body.get('action'), body.get('data'), body.get('value'))
  data = body.get('data')

  if action == 'insert':
    student = insert(data)
    if student:
      return JsonResponse({'student': student}, safe=False)
  elif action == 'insert_all':
    students = insert_all(data)
    if students:
      return JsonResponse({'students': students}, safe=False)
  elif action == 'update':
    student = update(data.get('id'), data.get('student'))
    if student:
      return JsonResponse({'student': student}, safe=False)
  elif action == 'fetch':
    student = fetch(data.get('id'))
    if student:
      return JsonResponse({'student': student}, safe=False)
  elif action in ['fetch_all_first_name', 'fetch_all_last_name', 'fetch_all_grade', 'fetch_all_age']:
    students = fetch_all(action, data.get('value'))
    if students:
      return JsonResponse({'students': students}, safe=False)
    else:
      return JsonResponse({'status': 'success', 'content': 'No students matching '+data.get('value')+'found'})
  elif action == 'undo_last':
    undo_last()
    return JsonResponse({'status': 'success'}, safe=False)
  else:
    return HttpResponseBadRequest(content='Invalid action')

def insert(student_data):
    # Create a new student and return their id
    student = Student.objects.create(**student_data)
    return student.id

def insert_all(students_data):
    # Create new students and return their ids
    students = [Student(**data) for data in students_data]
    Student.objects.bulk_create(students)
    return [student.id for student in students]

def update(id, student_data):
    # Update an existing student and return their id
    Student.objects.filter(id=id).update(**student_data)
    return id

def fetch(id):
    # Fetch a student by their id
    try:
        student = Student.objects.get(id=id)
        return {
            'id': student.id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'age': student.age,
            'grade': student.grade
        }
    except ObjectDoesNotExist:
        return None

def fetch_all(field, value):
    # Fetch all students by a given field and value
    field_mapping = {
        'fetch_all_first_name': 'first_name',
        'fetch_all_last_name': 'last_name',
        'fetch_all_age': 'age',
        'fetch_all_grade': 'grade'
    }
    students = Student.objects.filter(**{field_mapping[field]: value})
    return [{
        'id': student.id,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'age': student.age,
        'grade': student.grade
    } for student in students]

def undo_last():  # Django ORM does not support undoing operations, We should not use this in production
    # Undo the last operation by deleting the last student
    last_student = Student.objects.latest('id')
    last_student.delete()
