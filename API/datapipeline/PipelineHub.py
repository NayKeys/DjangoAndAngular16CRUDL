import sqlite3
import petl as etl
from django.http import JsonResponse
import ldap
import ldap.modlist as modlist

class Reference:
  pass

class ReferenceData:
  def __init__(self, dict):
    self.id = dict['id']
    self.reference = Reference()
    self.reference.first_name = dict['first_name']
    self.reference.last_name = dict['last_name']
    self.reference.role = dict['role']
    self.reference.age = dict['age']
    self.reference.grade = dict['grade']
    self.reference.homeaddress = dict['homeaddress']
  # def __init__(self, id: int, first_name: str, last_name: str, role: str, age: str, grade: str, address: str):
  #   self.id = id
  #   self.reference.first_name = first_name
  #   self.reference.first_name = first_name
  #   self.reference.last_name = last_name
  #   self.reference.role = role
  #   self.reference.age = age
  #   self.reference.grade = grade
  #   self.reference.homeaddress = homeaddress
  def toJson(self):
    return {
      "id": self.id,
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
  def __init__(self, status: str, message: str, data: ReferenceData):
    self.status = status
    self.message = message
    self.data = data
  def JsonResponse(self):
    if self.data == None:
      return JsonResponse({"status": self.status, "message": self.message}, status=self.status)
    return JsonResponse({"status": self.status, "message": self.message, "data": [ref.toJson() for ref in self.data]}, status=self.status)


import API.datapipeline.SQLPipeline as sql_pipeline
import API.datapipeline.CSVPipeline as csv_pipeline
import API.datapipeline.LDAPPipeline as ldap_pipeline

def fetch_all(reference: ReferenceData):
  try:
    fetched_data = []
    if (reference.get('role') != ""):
      fetched_data = sql_pipeline.fetch_all(reference)
    elif (reference.get('grade') != ""):
      fetched_data = csv_pipeline.fetch_all(reference)
    elif (reference.get('first_name') != ""):
      fetched_data = ldap_pipeline.fetch_all(reference)
    if (fetched_data):
      return ApiResponse(200, "Succesfuly retrieved elements", [ReferenceData(element) for element in fetched_data]).JsonResponse()
  except Exception as e:
    return ApiResponse(404, "No data found with this query role = "+reference.get('role')+"\n error-message: "+str(e)).JsonResponse()

def fetch(id: int, reference: ReferenceData):
  try: 
    if (id != ""):
      fetched_data = sql_pipeline.fetch(id)
    elif (reference.get('grade') != ""):
      fetched_data = csv_pipeline.fetch(id)
    elif (reference.get('first_name') != ""):
      fetched_data = ldap_pipeline.fetch(id)
    if (fetched_data):
      return ApiResponse(200, "Succesfuly retrieved element with id = "+str(id), [ReferenceData(element) for element in fetched_data]).JsonResponse()
  except Exception as e:
    return ApiResponse(404, "No data found with query id = "+str(id)+"\n error-message: "+str(e)).JsonResponse()

def delete(id: int, reference: ReferenceData):
  try:
    if (id != ""):
      petl_response = sql_pipeline.delete(id)
    elif (reference.get('grade') != ""):
      petl_response = csv_pipeline.delete(id)
    elif (reference.get('first_name') != ""):
      petl_response = ldap_pipeline.delete(id)
    if (petl_response):
      return ApiResponse(200, "Succesfuly deleted element with id = "+str(id), [ReferenceData(element) for element in petl_response]).JsonResponse()
  except Exception as e:
    return ApiResponse(500, "Couldnt delete element with id = "+str(id+"\n error-message: "+str(e)), None).JsonResponse()

def update(id: int, reference: ReferenceData):
  try:
    if (id != ""):
      petl_response = sql_pipeline.update(id, reference)
    elif (reference.get('grade') != ""):
      petl_response = csv_pipeline.update(id, reference)
    elif (reference.get('first_name') != ""):
      petl_response = ldap_pipeline.update(id, reference)
    if (petl_response):
      return ApiResponse(200, "Succesfuly updated element with id = "+str(id), [ReferenceData(element) for element in petl_response]).JsonResponse()
  except Exception as e:
    return ApiResponse(500, "Couldnt update element with id = "+str(id+"\n error-message: "+str(e)), None).JsonResponse()

def insert(reference: ReferenceData):
  try:
    if (reference.get('role') != ""):
      petl_response = sql_pipeline.insert(reference)
    elif (reference.get('grade') != ""):
      petl_response = csv_pipeline.insert(reference)
    if (petl_response):
      return ApiResponse(200, "Succesfuly created element", None).JsonResponse()
  except Exception as e:
    return ApiResponse(500, "Couldnt create element"+" \n error-message: "+str(e), None).JsonResponse()