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
    self.reference.address = dict['address']
  # def __init__(self, id: int, first_name: str, last_name: str, role: str, age: str, grade: str, address: str):
  #   self.id = id
  #   self.reference.first_name = first_name
  #   self.reference.first_name = first_name
  #   self.reference.last_name = last_name
  #   self.reference.role = role
  #   self.reference.age = age
  #   self.reference.grade = grade
  #   self.reference.address = address
  def toJson(self):
    return {
      "id": self.id,
      "reference": {
        "first_name": self.reference.first_name, "last_name": self.reference.last_name, "role": self.reference.role, "age": self.reference.age, "grade": self.reference.grade, "address": self.reference.address
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
    return JsonResponse({"status": self.status, "message": self.message, "data": [ref.toJson() for ref in self.data]}, status=self.status)


import SQLPipeline as sql_pipeline
import CSVPipeline as csv_pipeline
import LDAPPipeline as ldap_pipeline

def fetch_all(reference: ReferenceData):
  fetched_data = []
  if (reference.get('role') != ""):
    fetched_data = sql_pipeline.fetch_all(reference)
  elif (reference.get('grade') != ""):
    fetched_data = csv_pipeline.fetch_all(reference)
  elif (reference.get('first_name') != ""):
    fetched_data = ldap_pipeline.fetch_all(reference)
  if len(fetched_data) == 0:
    return ApiResponse(404, "No data found with query role = "+reference.get('role')).JsonResponse()
  return ApiResponse(200, "", [ReferenceData(element) for element in fetched_data]).JsonResponse()

def fetch(reference: ReferenceData):
  if (reference.get('id') != ""):
    fetched_data = sql_pipeline.fetch(reference)
  elif (reference.get('grade') != ""):
    fetched_data = csv_pipeline.fetch(reference)
  elif (reference.get('first_name') != ""):
    fetched_data = ldap_pipeline.fetch(reference)
  if len(fetched_data) == 0:
    return ApiResponse(404, "No data found with query id = "+reference.get('id')).JsonResponse()
  return ApiResponse(200, "Succesfuly retrieved element with id = +reference.get('id')", [ReferenceData(element) for element in fetched_data]).JsonResponse()

def delete(reference: ReferenceData):
  if (reference.get('id') != ""):
    sql_response = sql_pipeline.delete(reference)
  elif (reference.get('grade') != ""):
    sql_response = csv_pipeline.delete(reference)
  elif (reference.get('first_name') != ""):
    sql_response = ldap_pipeline.delete(reference)
  if len(sql_response) == 0:
    return ApiResponse(200, "(btw no data) Succesfuly deleted element with id = "+reference.get('id')).JsonResponse()
  return ApiResponse(200, "Succesfuly deleted element with id = ", [ReferenceData(element) for element in sql_response]).JsonResponse()

def updated(reference: ReferenceData):
  if (reference.get('id') != ""):
    sql_response = sql_pipeline.update(reference)
  elif (reference.get('grade') != ""):
    sql_response = csv_pipeline.update(reference)
  elif (reference.get('first_name') != ""):
    sql_response = ldap_pipeline.update(reference)
  if len(sql_response) == 0:
    return ApiResponse(200, "(btw no data) Succesfuly updated element with id = "+reference.get('id')).JsonResponse()
  return ApiResponse(200, "Succesfuly updated element with id = ", [ReferenceData(element) for element in sql_response]).JsonResponse()

def insert(reference: ReferenceData):  # This function is an example, feel free to adapt it to your needs and your database types
  if (reference.get('role') != ""):
    sql_response = sql_pipeline.insert(reference)
  elif (reference.get('grade') != ""):
    sql_response = csv_pipeline.insert(reference)
  elif (reference.get('first_name') != ""):
    sql_response = ldap_pipeline.insert(reference)
  if len(sql_response) == 0:
    return ApiResponse(200, "(btw no data) Succesfuly created element").JsonResponse()
  return ApiResponse(200, "Succesfuly created element", [ReferenceData(element) for element in sql_response]).JsonResponse()
