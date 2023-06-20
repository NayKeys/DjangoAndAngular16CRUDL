from django.shortcuts import render
import petl as etl
from django.http import JsonResponse
from django.db import connections

# Create your views here.

def fetch_data(request):
    with connections['default'].cursor() as cursor:
        cursor.execute("SELECT * FROM students_app_student")
        data = etl.fromdb(cursor, "SELECT * FROM students_app_student")
        # Assuming you want to filter the data where grade is greater than 2 and order by last name
        data = etl.select(data, lambda rec: rec['grade'] > 2)
        data = etl.sort(data, 'last_name')
        # Convert the filtered and sorted data to a list of dictionaries
        data = etl.dicts(data)
        return JsonResponse({'data': list(data)}, safe=False)
