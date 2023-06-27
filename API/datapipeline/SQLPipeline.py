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
def connect_sql(table: DBTable):
  conn = sqlite3.connect(table.databaseUrl)
  return conn

def fetch_all(reference):
  if (reference.get('role') == "all"):
    fetched_data = etl.fromdb(connect_sql(student_table), 'SELECT * FROM students_app_student')
    fetched_data = etl.dicts(etl.sort(fetched_data))
    return ApiResponse(200, "", [ReferenceData(element) for element in fetched_data]).JsonResponse()
  elif (reference.get('role') != ""):
    fetched_data = etl.fromdb(connect_sql(student_table), 'SELECT * FROM students_app_student WHERE role = ?', (reference.get('role'), ))
    fetched_data = etl.dicts(etl.sort(fetched_data))
  return fetched_data

def fetch(id: int):
  fetched_data = etl.fromdb(connect_sql(student_table), 'SELECT * FROM students_app_student WHERE id = ?', (id,))
  fetched_data = etl.dicts(etl.sort(fetched_data))
  return fetched_data

def delete(id: int):
  sql_response = etl.fromdb(connect_sql(student_table), 'DELETE FROM students_app_student WHERE id = ?', (id,))
  sql_response = etl.dicts(etl.sort(sql_response))
  return True

def update(id: int, updated_reference: ReferenceData):
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
  cursor = connect_sql(student_table).cursor()
  output = cursor.execute('UPDATE students_app_student SET '+query+' WHERE id = ?', (id,))
  return True

def insert(reference: ReferenceData):
  to_be_inserted = etl.fromdicts([reference], header=['first_name', 'last_name', 'role', 'age', 'grade'])  # Id is autoincremented
  etl.todb(to_be_inserted, connect_sql(student_table), student_table.tableName, create='True', commit=True)
  return True