from django.http import JsonResponse
import petl as etl

""" NOTE:
  Functions should returns a Dictionary instead of a JSON Api response directly (DONE)
"""

class ApiRequest:
  def __init__(self, json):
    self.action = json['action']
    self.jwt = json['jwt']
    self.view_name = json['view_name']
    self.row = json['row']

class ApiResponse:
  def __init__(self, status: int, message: str, rows: dict = None):
    self.status = status
    self.message = message
    if rows is None:
      self.row_keys = None
      self.rows = None
    else:
      self.row_keys = list(rows[0].keys())
      self.rows = [list(row.values()) for row in rows]
  def json_response(self):
    if self.rows is None:
      return JsonResponse({"status": self.status, "message": self.message}, status=self.status)
    return JsonResponse({"status": self.status, "message": self.message, "row_keys": self.row_keys, "rows": self.rows}, status=self.status)

import datahub.pipelines.SQLPipeline as sql_pipeline
import datahub.pipelines.CSVPipeline as csv_pipeline
import datahub.pipelines.LDAPPipeline as ldap_pipeline
import datahub.config as config

def fetch_all(view_name: str):
  if not view_name in config.VIEW_LIST.keys():
    print('Error: View does not exists: '+view_name)
    return None
  view = config.VIEW_LIST[view_name]
  match view["method"]:
    case "sql":
      dict_list = sql_pipeline.fetch_all(view)
      return dict_list
    case "csv":
      dict_list = csv_pipeline.fetch_all(view)
      return dict_list
    case "ldap":
      dict_list = ldap_pipeline.fetch_all(view)
      return dict_list

def fetch(view_name: str, row: dict):
  if not view_name in config.VIEW_LIST.keys():
    print('Error: View does not exists: '+view_name)
    return None
  view = config.VIEW_LIST[view_name]
  match view["method"]:
    case "sql":
      identifier = row[view['identifier_name']]
      dict_list = sql_pipeline.fetch(view, identifier)
      return dict_list
    case "csv":
      identifier = row[0]  # Indice of line in csv file is expected to be first column of row
      dict_list = csv_pipeline.fetch(view, identifier)
      return dict_list
    case "ldap":
      identifier = row[view['identifier_name']]
      dict_list = ldap_pipeline.fetch(view, identifier)
      return dict_list

def delete(view_name: str, row: dict):
  if not view_name in config.VIEW_LIST.keys():
    print('Error: View does not exists: '+view_name)
    return None
  view = config.VIEW_LIST[view_name]
  match view["method"]:
    case "sql":
      identifier = row[view['identifier_name']]
      dict_list = sql_pipeline.delete(view, identifier)
      return dict_list
    case "csv":
      identifier = row[0]  # Indice of line in csv file is expected to be first column of row
      dict_list = csv_pipeline.delete(view, identifier)
      return dict_list
    case "ldap":
      identifier = row[view['identifier_name']]
      dict_list = ldap_pipeline.delete(view, identifier)
      return dict_list

def insert(view_name: str, row: dict):
  if not view_name in config.VIEW_LIST.keys():
    print('Error: View does not exists: '+view_name)
    return None
  view = config.VIEW_LIST[view_name]
  match view["method"]:
    case "sql":
      dict_list = sql_pipeline.delete(view, row)
      return dict_list
    case "csv":
      dict_list = csv_pipeline.delete(view, row)
      return dict_list
    case "ldap":
      dict_list = ldap_pipeline.delete(view, row)
      return dict_list

def update(view_name: str, row: dict):
  if not view_name in config.VIEW_LIST.keys():
    print('Error: View does not exists: '+view_name)
    return None
  view = config.VIEW_LIST[view_name]
  match view["method"]:
    case "sql":
      identifier = row[view['identifier_name']]
      dict_list = sql_pipeline.update(view, identifier, row)
      return dict_list
    case "csv":
      identifier = row[0]  # Indice of line in csv file is expected to be first column of row
      dict_list = csv_pipeline.update(view, identifier, row)
      return dict_list
    case "ldap":
      identifier = row[view['identifier_name']]
      dict_list = ldap_pipeline.update(view, identifier, row)
      return dict_list

def check_permission_create(user, view_name, data):
  print(f'user with username {user.username} with role {user.role} wants to create element {data} in the view {view_name}')
  return True

def check_permission_update(user, view_name, data):
  print(f'user with username {user.username} with role {user.role} wants to update element {data} in the view {view_name}')
  return True

def check_permission_delete(user, view_name, data):
  print(f'user with username {user.username} with role {user.role} wants to delete element {data} in the view {view_name}')
  return True

def check_permission_fetch(user, view_name, data):
  print(f'user with username {user.username} with role {user.role} wants to fetch element {data} in the view {view_name}')
  return True

def check_permission_fetch_all(user, view_name, data):
  print(f'user with username {user.username} with role {user.role} wants to fetch all elements of the view {view_name}')
  return True