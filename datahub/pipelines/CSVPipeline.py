import os
import json
import sqlite3
import petl as etl
from django.http import JsonResponse

CSV_PATH = 'students.csv'  # path to your CSV file


def connect_to_db():
    conn = sqlite3.connect('db.sqlite3')
    return conn


def insert(student):
    conn = connect_to_db()
    table = etl.fromdicts(
        [student], header=['id', 'first_name', 'last_name', 'age', 'grade'])
    etl.todb(table, conn, 'students_app_student', create='False', commit=True)

    if os.path.exists(CSV_PATH):
        csv_table = etl.fromcsv(CSV_PATH)
        csv_table = etl.cat(csv_table, table)
    else:
        csv_table = table

    etl.tocsv(csv_table, CSV_PATH)
    return JsonResponse({"status": "Inserted"}, status=200)


def insert_all(students):
    conn = connect_to_db()
    table = etl.fromdicts(
        students, header=['id', 'first_name', 'last_name', 'age', 'grade'])
    etl.todb(table, conn, 'students_app_student', create='False', commit=True)

    if os.path.exists(CSV_PATH):
        csv_table = etl.fromcsv(CSV_PATH)
        csv_table = etl.cat(csv_table, table)
    else:
        csv_table = table

    etl.tocsv(csv_table, CSV_PATH)
    return JsonResponse({"status": "Inserted all"}, status=200)


def update(id, student):
    conn = connect_to_db()
    table = etl.fromdb(conn, 'SELECT * FROM students_app_student')
    table = etl.update(table, 'id', id, student)
    etl.todb(table, conn, 'students_app_student', create='False', commit=True)

    csv_table = etl.fromcsv(CSV_PATH)
    csv_table = etl.update(csv_table, 'id', id, student)
    etl.tocsv(csv_table, CSV_PATH)

    return JsonResponse({"status": "Updated"}, status=200)


def remove(id):
    conn = connect_to_db()
    table = etl.fromdb(
        conn, 'SELECT * FROM students_app_student WHERE id != ?', (id,))
    etl.todb(table, conn, 'students_app_student', create='False', commit=True)

    csv_table = etl.fromcsv(CSV_PATH)
    csv_table = etl.select(csv_table, lambda rec: rec.id != id)
    etl.tocsv(csv_table, CSV_PATH)

    return JsonResponse({"status": "Removed"}, status=200)


def fetch_all(field):
    conn = connect_to_db()
    table = etl.fromdb(conn, 'SELECT * FROM students_app_student')
    table = etl.sort(table, field)
    return JsonResponse(etl.dicts(table), safe=False)


def fetch(id):
    conn = connect_to_db()
    table = etl.fromdb(
        conn, 'SELECT * FROM students_app_student WHERE id = ?', (id,))
    return JsonResponse(etl.dicts(table), safe=False)
