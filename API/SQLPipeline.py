import petl as etl
import sqlite3
from PipelineHub import ApiResponse, ReferenceData

class DBTable:
  def __init__(self, tableName, databaseUrl, dn=None, password=None):
    self.tableName = tableName
    # URL Completed with the authentification informations protocol://url:server@user:password
    self.databaseUrl = databaseUrl
    self.dn = dn
    self.password = password

''' We could imagine defining here the db tables that we will be used '''
student_table = DBTable('students_app_student', 'studentsDB.sqlite3')  # URL Completed with the authentification informations protocol://url:server@user:password
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

def fetch(reference):
  fetched_data = etl.fromdb(connect_sql(student_table), 'SELECT * FROM students_app_student WHERE id = ?', (reference.get('id'),))
  fetched_data = etl.dicts(etl.sort(fetched_data))
  return fetched_data

def delete(reference):
  sql_response = etl.fromdb(connect_sql(student_table), 'DELETE FROM students_app_student WHERE id = ?', (reference.get('id'),))
  sql_response = etl.dicts(etl.sort(sql_response))
  return sql_response

def update(reference: ReferenceData, updated_reference: ReferenceData):
  data_to_be_updated = etl.fromdb(connect_sql(student_table), 'SELECT * FROM students_app_student WHERE id = ?', (reference.get('id'),))
  if len(data_to_be_updated) == 0:
    return ApiResponse(404, "No data found with query id = "+reference.get('id')).JsonResponse()
  updated_data = data_to_be_updated[0]
  for key in updated_reference.keys():
    updated_data = etl.update(updated_data, key, updated_reference[key])
  return etl.todb(updated_data, connect_sql(student_table),'students_app_student', create='False', commit=True)

def insert(reference: ReferenceData):
  to_be_inserted = etl.fromdicts([reference], header=['id', 'first_name', 'last_name', 'role', 'age', 'grade'])
  return etl.todb(to_be_inserted, connect_sql(student_table), student_table.tableName, create='True', commit=True)