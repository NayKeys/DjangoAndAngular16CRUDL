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

def fetch(id: int):
  conn = sqlite3.connect(student_table.databaseUrl)
  fetched_data = etl.fromdb(conn, 'SELECT * FROM students_app_student WHERE id = ?', (id,))
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
  query = ''
  for key in updated_reference.keys():  # Editing old row with new values
    updated_value = updated_reference.get(key)
    if updated_value == "":
      continue
    if re.match('^[0-9]+$', str(updated_value)):  # If contains only numbers (if digit)
      query += key + ' = ' + str(updated_value) + ', '
    else:  # If digit no quotes
      query += key + ' = "' + str(updated_value) + '", '
  query = query[:-2]  # Removing last comma
  cursor = conn.cursor()
  output = cursor.execute('UPDATE students_app_student SET '+query+' WHERE id = ?', (id,))
  conn.commit()
  return True

def insert(reference: ReferenceData):
  conn = sqlite3.connect(student_table.databaseUrl)
  to_be_inserted = etl.fromdicts([reference], header=['first_name', 'last_name', 'role', 'age', 'grade'])  # Id is autoincremented
  etl.todb(to_be_inserted, conn, student_table.tableName, create='True', commit=True)
  conn.commit()
  return True