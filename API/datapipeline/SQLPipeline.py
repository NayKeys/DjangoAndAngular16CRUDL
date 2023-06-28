import petl as etl
import sqlite3
from API.datapipeline.PipelineHub import ApiResponse, ReferenceData
import re
import sqlite3

class DBTable:
  def __init__(self, tableName, databaseUrl, dn=None, password=None):
    self.tableName = tableName
    # URL Completed with the authentification informations protocol://url:server@user:password
    self.databaseUrl = databaseUrl
    self.dn = dn
    self.password = password

''' We could imagine defining here the db tables that we will be used '''
student_table = DBTable('students_app_student', 'studentsDB.sqlite3')  # URL Complete with the authentification informations protocol://url:server@user:password

def fetch_all(reference):
  if (reference.get('role') == "all"):
    conn = sqlite3.connect(student_table.databaseUrl)
    fetched_data = etl.fromdb(conn, 'SELECT * FROM students_app_student')
    fetched_data = etl.dicts(etl.sort(fetched_data))
    conn.commit()
    return ApiResponse(200, "", [ReferenceData(element) for element in fetched_data]).JsonResponse()
  elif (reference.get('role') != ""):
    conn = sqlite3.connect(student_table.databaseUrl)
    fetched_data = etl.fromdb(conn, 'SELECT * FROM students_app_student WHERE role = ?', (reference.get('role'), ))
    fetched_data = etl.dicts(etl.sort(fetched_data))
    conn.commit()
    return fetched_data

def fetchByID(id: int):
  conn = sqlite3.connect(student_table.databaseUrl)
  fetched_data = etl.fromdb(conn, 'SELECT * FROM students_app_student WHERE id = ?', (id,))
  fetched_data = etl.dicts(etl.sort(fetched_data))
  conn.commit()
  return fetched_data

def fetchByUsername(username: str):
  conn = sqlite3.connect(student_table.databaseUrl)
  fetched_data = etl.fromdb(conn, 'SELECT * FROM students_app_student WHERE username = ?', (username,))
  fetched_data = etl.dicts(etl.sort(fetched_data))
  conn.commit()
  return fetched_data

def delete(id: int):
  conn = sqlite3.connect(student_table.databaseUrl)
  cursor = conn.cursor()
  cursor.execute('DELETE FROM students_app_student WHERE id = ?', (id,))
  cursor.fetchall()
  conn.commit()
  return True

def update(id: int, updated_reference: ReferenceData):
  conn = sqlite3.connect(student_table.databaseUrl)
  cursor = conn.cursor()
  output = cursor.execute('UPDATE students_app_student SET first_name = ?, last_name = ?, role = ?, age = ?, grade = ?, homeaddress = ?WHERE id = ?', (updated_reference.get('first_name'), updated_reference.get('last_name'), updated_reference.get('role'), updated_reference.get('age'), updated_reference.get('grade'), updated_reference.get('homeaddress'), id))
  conn.commit()
  return True

def insert(new_reference: ReferenceData):
  conn = sqlite3.connect(student_table.databaseUrl)
  cursor = conn.cursor()
  output = cursor.execute('INSERT INTO students_app_student (first_name, last_name, role, age, grade, homeaddress) VALUES (?, ?, ?, ?, ?, ?)', (new_reference.get('first_name'), new_reference.get('last_name'), new_reference.get('role'), new_reference.get('age'), new_reference.get('grade'), new_reference.get('homeaddress')))
  conn.commit()
  return True