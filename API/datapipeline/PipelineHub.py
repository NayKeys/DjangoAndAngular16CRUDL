import petl as etl
from django.http import JsonResponse
import ldap.modlist as modlist
import petl as etl

""" NOTE:
  Functions should returns a Dictionary instead of a JSON Api response directly (DONE)
"""

class Reference:
  def from_dict(dict):
    return Reference(dict['first_name'], dict['last_name'], dict['role'], dict['age'], dict['grade'], dict['homeaddress'])
  def __init__(self, first_name: str = "", last_name: str = "", role: str = "", age: int = 0, grade: int = 1, homeaddress: str = ""):
    self.first_name = first_name
    self.first_name = first_name
    self.last_name = last_name
    self.role = role
    self.age = age
    self.grade = grade
    self.homeaddress = homeaddress

class ReferenceData:
  def from_flat_dicts(element):
    return ReferenceData(element['id'], element['username'], element['first_name'], element['last_name'], element['role'], element['age'], element['grade'], element['homeaddress'])
  def fromDict(dict):
    return ReferenceData(dict['id'], dict['username'], dict['reference']['first_name'], dict['reference']['last_name'], dict['reference']['role'], dict['reference']['age'], dict['reference']['grade'], dict['reference']['homeaddress'])
  def __init__(self, ID: int = 0, username: str = "", first_name: str = "", last_name: str = "", role: str = "", age: int = 0, grade: int = 1, homeaddress: str = ""):
    self.id = ID
    self.username = username
    self.reference = Reference(first_name, last_name, role, age, grade, homeaddress)
  def toDict(self):
    return {
      "id": self.id,
      "username": self.username,
      "reference": {
        "first_name": self.reference.first_name, "last_name": self.reference.last_name, "role": self.reference.role, "age": self.reference.age, "grade": self.reference.grade, "homeaddress": self.reference.homeaddress
      }
    }

class ApiRequest:
  def __init__(self, action: str, jwt: str, data: ReferenceData):
    self.action = action
    self.jwt = jwt
    self.data = data
  def __init__(self, json):
    self.action = json['action']
    self.jwt = json['jwt']
    self.data = json['data']

class ApiResponse:
  def __init__(self, status: int, message: str, data: ReferenceData):
    self.status = status
    self.message = message
    self.data = data
  def JsonResponse(self):
    if self.data == None:
      return JsonResponse({"status": self.status, "message": self.message}, status=self.status)
    return JsonResponse({"status": self.status, "message": self.message, "data": [ref.toDict() for ref in self.data]}, status=self.status)


import API.datapipeline.SQLPipeline as sql_pipeline
import API.datapipeline.CSVPipeline as csv_pipeline
import API.datapipeline.LDAPPipeline as ldap_pipeline

def fetch_all(reference: ReferenceData):
  fetched_data = []
  if (reference.reference.role != ""):
    fetched_data = sql_pipeline.fetch_all(reference)
  elif (reference.reference.grade != ""):
    fetched_data = csv_pipeline.fetch_all(reference)
  elif (reference.reference.first_name != ""):
    fetched_data = ldap_pipeline.fetch_all(reference)
  return fetched_data

def fetch(reference: ReferenceData):
  if (reference.id):
    fetched_data = sql_pipeline.fetchByID(reference.id)
  elif (reference.username):
    fetched_data = sql_pipeline.fetchByUsername(reference.username)
  elif (reference.reference.grade != ""):
    fetched_data = csv_pipeline.fetch(id)
  elif (reference.reference.first_name != ""):
    fetched_data = ldap_pipeline.fetch(id)
  return fetched_data

def delete(reference: ReferenceData):
  if (reference.id != ""):
    petl_response = sql_pipeline.delete(reference.id)
  elif (reference.reference.grade != ""):
    petl_response = csv_pipeline.delete(reference.id)
  elif (reference.reference.first_name != ""):
    petl_response = ldap_pipeline.delete(reference.id)
  return petl_response

def update(reference: ReferenceData):
  if (reference.id != ""):
    petl_response = sql_pipeline.update(reference.id, reference)
  elif (reference.reference.grade != ""):
    petl_response = csv_pipeline.update(reference.id, reference)
  elif (reference.reference.first_name != ""):
    petl_response = ldap_pipeline.update(reference.id, reference)
  return petl_response

def insert(reference: ReferenceData):
  if (reference.reference.role != ""):
    petl_response = sql_pipeline.insert(reference)
  elif (reference.reference.grade != ""):
    petl_response = csv_pipeline.insert(reference)
  return petl_response

def check_permission_create(data, user):
  print('user with username {} with role {} wants to create reference {} in the database'.format(user.username, user.reference.role, data.username))
  return True

def check_permission_update(data, user):
  print('user with username {} with role {} wants to update reference {} in the database'.format(user.username, user.reference.role, data.username))
  return True

def check_permission_delete(data, user):
  print('user with username {} with role {} wants to delete reference {} in the database'.format(user.username, user.reference.role, data.username))
  return True

def check_permission_fetch(data, user):
  print('user with username {} with role {} wants to fetch reference {} in the database'.format(user.username, user.reference.role, data.username))
  return True

def check_permission_fetch_all(data, user):
  print('user with username {} with role {} wants to fetch all references with role {} in the database'.format(user.username, user.reference.role, data.reference.role))
  return True