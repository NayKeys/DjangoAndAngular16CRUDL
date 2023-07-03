import petl as etl
import sqlite3
from datahub.pipelines.hub import ApiResponse
import re
import sqlite3
import json

class DBTable:
  def __init__(self, tableName, databaseUrl, dn=None, password=None):
    self.tableName = tableName
    # URL Completed with the authentification informations protocol://url:server@user:password
    self.databaseUrl = databaseUrl
    self.dn = dn
    self.password = password

def fetch_all(table: dict):
  conn = sqlite3.connect(table['database_url'])
  fetched_data = etl.fromdb(conn, f'SELECT * FROM {table["table_name"]}')
  fetched_data = etl.dicts(etl.sort(fetched_data))
  conn.commit()
  if (len(fetched_data) == 0):
    return None
  return fetched_data

def fetch(table: dict, identifier: str):
  conn = sqlite3.connect(table['database_url'])
  fetched_data = etl.fromdb(conn, f'SELECT 1 FROM {table["table_name"]} WHERE {table["identifier_name"]} = ?', (identifier,))
  fetched_data = etl.dicts(etl.sort(fetched_data))
  conn.commit()
  if (len(fetched_data) == 0):
    return None
  return fetched_data

def delete(table: dict, identifier: str):
  conn = sqlite3.connect(table['database_url'])
  cursor = conn.cursor()
  cursor.execute(f'DELETE FROM {table["table_name"]} WHERE {table["identifier_name"]} = ?', (identifier,))
  cursor.fetchall()
  conn.commit()
  return True

def update(table: dict, identifier: str, updated_element: dict):
  conn = sqlite3.connect(table['database_url'])
  cursor = conn.cursor()
  # Delete eventual un-updatable columns
  # del updated_element[updated_element['identifier_name']]
  del updated_element['id']
  output = cursor.execute(f'UPDATE {table["table_name"]} SET {", ".join([f"{key} = ?" for key in updated_element.keys()])} WHERE {table["identifier_name"]} = ?', tuple(updated_element.values()) + (identifier,))
  conn.commit()
  return True

def insert(table: dict, new_element: dict):
  conn = sqlite3.connect(table['database_url'])
  cursor = conn.cursor()
  columns = [element[1] for element in cursor.execute(f'PRAGMA table_info({table["table_name"]})')]
  for key in new_element.keys():
    if (key not in columns):
      return f"Error: This column '{key}' doesn't exist in the table '{table['table_name']}'"
  output = cursor.execute(f'INSERT INTO {table["table_name"]} ({", ".join(new_element.keys())}) VALUES ({", ".join(["?" for i in range(len(new_element.keys()))])})', tuple(new_element.values()))
  conn.commit()
  return True