import json
import sqlite3
import petl as etl
from django.http import JsonResponse

def connect_to_db():
    conn = sqlite3.connect('studentDB.sqlite3')
    return conn

def execute(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        
        if action == 'insert':
            student = data.get('student')
            return insert(student)

        elif action == 'insert_all':
            students = data.get('students')
            return insert_all(students)

        elif action == 'update':
            id = data.get('id')
            student = data.get('student')
            return update(id, student)

        elif action == 'fetch_all':
            field = data.get('field')
            return fetch_all(field)
            
        elif action == 'fetch':
            id = data.get('id')
            return fetch(id)

    else:
        return JsonResponse({"error": "Invalid method"}, status=400)

def insert(student):
    conn = connect_to_db()
    table = etl.fromdicts([student], header=['id', 'first_name', 'last_name', 'age', 'grade'])
    etl.todb(table, conn, 'students_app_student', create='False', commit=True)
    return JsonResponse({"status": "Inserted"}, status=200)

def insert_all(students):
    conn = connect_to_db()
    table = etl.fromdicts(students, header=['id', 'first_name', 'last_name', 'age', 'grade'])
    etl.todb(table, conn, 'students_app_student', create='False', commit=True)
    return JsonResponse({"status": "Inserted all"}, status=200)

def update(id, student):
    conn = connect_to_db()
    table = etl.fromdb(conn, 'SELECT * FROM students_app_student')
    table = etl.update(table, 'id', id, student)
    etl.todb(table, conn, 'students_app_student', create='False', commit=True)
    return JsonResponse({"status": "Updated"}, status=200)

def fetch_all(field):
    conn = connect_to_db()
    table = etl.fromdb(conn, 'SELECT * FROM students_app_student')
    table = etl.sort(table, field)
    return JsonResponse(etl.dicts(table), safe=False)

def fetch(id):
    conn = connect_to_db()
    table = etl.fromdb(conn, 'SELECT * FROM students_app_student WHERE id = ?', (id,))
    return JsonResponse(etl.dicts(table), safe=False)



# from django.shortcuts import render
# import petl as etl
# from django.http import JsonResponse, HttpResponseBadRequest
# from django.core.exceptions import ObjectDoesNotExist
# from django.views.decorators.csrf import csrf_exempt
# import json
# from django.forms.models import model_to_dict


# # Create your views here.

# from .models import Student

# from django.core import serializers

# def fetch_all(request):
#   students = Student.objects.all()
#   data = serializers.serialize('json', students)
#   return JsonResponse(data, safe=False)


# @csrf_exempt
# def execute(request):
#   body_unicode = request.body.decode('utf-8')
#   body = json.loads(body_unicode)
#   action = body.get('action')
#   print('api/execute : executing', body.get('action'), body.get('data'), body.get('value'))
#   data = body.get('data')

#   if action == 'insert':
#     student = insert(data)
#     if student:
#       return JsonResponse({'student': student}, safe=False)
#   elif action == 'insert_all':
#     students = insert_all(data)
#     if students:
#       return JsonResponse({'students': students}, safe=False)
#   elif action == 'update':
#     student = update(data.get('id'), data.get('student'))
#     if student:
#       return JsonResponse({'student': student}, safe=False)
#   elif action == 'fetch':
#     student = fetch(data.get('id'))
#     if student:
#       return JsonResponse({'student': student}, safe=False)
#   elif action in ['fetch_all_first_name', 'fetch_all_last_name', 'fetch_all_grade', 'fetch_all_age']:
#     students = fetch_all(action, data.get('value'))
#     if students:
#       return JsonResponse({'students': students}, safe=False)
#     else:
#       return JsonResponse({'status': 'success', 'content': 'No students matching '+data.get('value')+'found'})
#   elif action == 'undo_last':
#     undo_last()
#     return JsonResponse({'status': 'success'}, safe=False)
#   else:
#     return HttpResponseBadRequest(content='Invalid action')

# def fetch_all(request):
#     students = list(Student.objects.values()) # converts QuerySet to list of dicts
#     return JsonResponse(students, safe=False)

# def fetch(request):
#     id = request.POST['id']
#     try:
#         student = Student.objects.get(id=id)
#         return JsonResponse(model_to_dict(student))  # Convert model instance to dict
#     except Student.DoesNotExist:
#         return JsonResponse({'error': 'Student not found'}, status=404)

# def insert(request):
#     student_data = request.POST['student']
#     student = Student.objects.create(**student_data)
#     return JsonResponse(model_to_dict(student))  # Return the created student

# def insert_all(request):
#     students_data = request.POST['students']
#     students = [Student(**data) for data in students_data]
#     Student.objects.bulk_create(students)
#     return JsonResponse({'message': 'Students created'}, status=201)

# def update(request):
#     id = request.POST['id']
#     student_data = request.POST['student']
#     try:
#         student = Student.objects.get(id=id)
#         for key, value in student_data.items():
#             setattr(student, key, value)
#         student.save()
#         return JsonResponse(model_to_dict(student))  # Return the updated student
#     except Student.DoesNotExist:
#         return JsonResponse({'error': 'Student not found'}, status=404)


# def undo_last():  # Django ORM does not support undoing operations, We should not use this in production
#     # Undo the last operation by deleting the last student
#     last_student = Student.objects.latest('id')
#     last_student.delete()