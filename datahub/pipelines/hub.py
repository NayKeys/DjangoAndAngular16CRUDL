from django.http import JsonResponse
import petl as etl

""" NOTE:
  Functions should returns a Dictionary instead of a JSON Api response directly (DONE)
"""

class ApiRequest:
  def __init__(self, json):
    self.action = json['action']
    self.jwt = json['jwt']
    self.data = json['data']

class ApiResponse:
  def __init__(self, status: int, message: str, data: dict = None):
    self.status = status
    self.message = message
    self.data = data
  def json_response(self):
    if self.data is None:
      return JsonResponse({"status": self.status, "message": self.message}, status=self.status)
    return JsonResponse({"status": self.status, "message": self.message, "data": self.data}, status=self.status)

SQL_TABLES = [
  {
    "table_name": "students_app_student",
    "database_url": "studentsDB.sqlite3",
    "identifier_name": "id",
  }
]
CSV_FILES = ["view1.csv", "view2.csv"]
LDAP_ENDPOINT = ["dc=org1", "dc=org2"]  # This is just an example I don't have any idea of what I just typed here

import datahub.pipelines.SQLPipeline as sql_pipeline
import datahub.pipelines.CSVPipeline as csv_pipeline
import datahub.pipelines.LDAPPipeline as ldap_pipeline

def fetch_all(view_name: str):
  if (view_name == "sql_view_1"):
    dict_list = sql_pipeline.fetch_all(SQL_TABLES[0])  # Passing table name as parameter
  elif (view_name == "csv_view_1"):
    dict_list = csv_pipeline.fetch_all(CSV_FILES[0])  # Choosing which csv file to fetch
  elif (view_name == "csv_view_2"):
    dict_list = csv_pipeline.fetch_all(CSV_FILES[1])
  elif (view_name == "ldap_view_1"):
    dict_list = ldap_pipeline.fetch_all(LDAP_ENDPOINT[0])
  elif (view_name == "ldap_view_1"):
    dict_list = ldap_pipeline.fetch_all(LDAP_ENDPOINT[1])
  return dict_list

def fetch(view_name: str, identifier: str):
  if (view_name == "sql_view_1"):
    dict_list = sql_pipeline.fetch(SQL_TABLES[0], identifier)
  elif (view_name == "csv_view_1"):
    dict_list = csv_pipeline.fetch(CSV_FILES[0], identifier)
  elif (view_name == "csv_view_2"):
    dict_list = csv_pipeline.fetch(CSV_FILES[1], identifier)
  elif (view_name == "ldap_view_1"):
    dict_list = ldap_pipeline.fetch(LDAP_ENDPOINT[0], identifier)
  elif (view_name == "ldap_view_1"):
    dict_list = ldap_pipeline.fetch(LDAP_ENDPOINT[1], identifier)
  return dict_list

def delete(view_name: str, identifier: str):
  if (view_name == "sql_view_1"):
    response = sql_pipeline.delete(SQL_TABLES[0], identifier)
  elif (view_name == "csv_view_1"):
    response = csv_pipeline.delete(CSV_FILES[0], identifier)
  elif (view_name == "csv_view_2"):
    response = csv_pipeline.delete(CSV_FILES[1], identifier)
  elif (view_name == "ldap_view_1"):
    response = ldap_pipeline.delete(LDAP_ENDPOINT[0], identifier)
  elif (view_name == "ldap_view_1"):
    response = ldap_pipeline.delete(LDAP_ENDPOINT[1], identifier)
  return response

def insert(view_name: str, data: dict):
  if (view_name == "sql_view_1"):
    response = sql_pipeline.insert(SQL_TABLES[0], data)
  elif (view_name == "csv_view_1"):
    response = csv_pipeline.insert(CSV_FILES[0], data)
  elif (view_name == "csv_view_2"):
    response = csv_pipeline.insert(CSV_FILES[1], data)
  elif (view_name == "ldap_view_1"):
    response = ldap_pipeline.insert(LDAP_ENDPOINT[0], data)
  elif (view_name == "ldap_view_1"):
    response = ldap_pipeline.insert(LDAP_ENDPOINT[1], data)
  return response

def update(view_name: str, identifier: str, data: dict):
  if (view_name == "sql_view_1"):
    response = sql_pipeline.update(SQL_TABLES[0], identifier, data)
  elif (view_name == "csv_view_1"):
    response = csv_pipeline.update(CSV_FILES[0], identifier, data)
  elif (view_name == "csv_view_2"):
    response = csv_pipeline.update(CSV_FILES[1], identifier, data)
  elif (view_name == "ldap_view_1"):
    response = ldap_pipeline.update(LDAP_ENDPOINT[0], identifier, data)
  elif (view_name == "ldap_view_1"):
    response = ldap_pipeline.update(LDAP_ENDPOINT[1], identifier, data)
  return response

def check_permission_create(data, user):
  print('user with username {} with role {} wants to create reference {} in the database'.format(user.username, user.role, data))
  return True

def check_permission_update(data, user):
  print('user with username {} with role {} wants to update reference {} in the database'.format(user.username, user.role, data))
  return True

def check_permission_delete(data, user):
  print('user with username {} with role {} wants to delete reference {} in the database'.format(user.username, user.role, data))
  return True

def check_permission_fetch(data, user):
  print('user with username {} with role {} wants to fetch reference {} in the database'.format(user.username, user.role, data))
  return True

def check_permission_fetch_all(data, user):
  print('user with username {} with role {} wants to fetch all references with role {} in the database'.format(user.username, user.role, data))
  return True