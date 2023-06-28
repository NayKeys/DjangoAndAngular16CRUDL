import petl as etl
from django.http import JsonResponse
import ldap.modlist as modlist

""" NOTE:
  Functions should returns a Dictionary instead of a JSON Api response directly (DONE)
"""

class Reference:
  pass

class ReferenceData:
  def fromDict(dict):
    return ReferenceData(dict['id'], dict['username'], dict['first_name'], dict['last_name'], dict['role'], dict['age'], dict['grade'], dict['homeaddress'])
  
  def __init__(self, id: int = 0, username: str = "", first_name: str = "", last_name: str = "", role: str = "", age: int = 0, grade: int = 1, homeaddress: str = ""):
    self.id = id
    self.username = username
    self.reference = Reference()
    self.reference.first_name = first_name
    self.reference.first_name = first_name
    self.reference.last_name = last_name
    self.reference.role = role
    self.reference.age = age
    self.reference.grade = grade
    self.reference.homeaddress = homeaddress
  
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
  if (reference.role != ""):
    fetched_data = sql_pipeline.fetch_all(reference)
  elif (reference.grade != ""):
    fetched_data = csv_pipeline.fetch_all(reference)
  elif (reference.first_name != ""):
    fetched_data = ldap_pipeline.fetch_all(reference)
  return fetched_data

def fetch(reference: ReferenceData):
  if (reference.id):
    fetched_data = sql_pipeline.fetchByID(reference.id)
  elif (reference.username):
    fetched_data = sql_pipeline.fetchByUsername(reference.username)
  elif (reference.grade != ""):
    fetched_data = csv_pipeline.fetch(id)
  elif (reference.first_name != ""):
    fetched_data = ldap_pipeline.fetch(id)
  return fetched_data

def delete(reference: ReferenceData):
  if (reference.id != ""):
    petl_response = sql_pipeline.delete(reference.id)
  elif (reference.grade != ""):
    petl_response = csv_pipeline.delete(reference.id)
  elif (reference.first_name != ""):
    petl_response = ldap_pipeline.delete(reference.id)
  return petl_response

def update(reference: ReferenceData):
  if (reference.id != ""):
    petl_response = sql_pipeline.update(reference.id, reference)
  elif (reference.grade != ""):
    petl_response = csv_pipeline.update(reference.id, reference)
  elif (reference.first_name != ""):
    petl_response = ldap_pipeline.update(reference.id, reference)
  return petl_response

def insert(reference: ReferenceData):
  if (reference.role != ""):
    petl_response = sql_pipeline.insert(reference)
  elif (reference.grade != ""):
    petl_response = csv_pipeline.insert(reference)
  return petl_response