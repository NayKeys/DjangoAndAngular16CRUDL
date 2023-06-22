import sqlite3
import petl as etl
from django.http import JsonResponse
import ldap
import ldap.modlist as modlist

class DBTable:
  def __init__(self, tableName, databaseUrl, dn = None, password = None):
    self.tableName = tableName
    self.databaseUrl = databaseUrl  # URL Completed with the authentification informations protocol://url:server@user:password
    self.dn = dn
    self.password = password


''' We could imagine defining here the db tables that we will be used '''
student_table = DBTable('students_app_student', 'studentsDB.sqlite3')  # URL Completed with the authentification informations protocol://url:server@user:password

def connect_sql(table: DBTable):
  conn = sqlite3.connect(table.databaseUrl)
  return conn

def connect_ldap(table):
  # Initialize a connection to the LDAP server
  conn = ldap.initialize(table.databaseUrl)
  # Bind (authenticate) to the server
  # Replace 'cn=admin,dc=example,dc=com' and 'password' with your DN and password
  conn.simple_bind_s(table.dn, table.password)
  return conn

def searchLDAP(table, baseDN, query):
  # Perform a search
  # Replace 'dc=example,dc=com' with your base DN
  # Replace '(objectclass=person)' with your search filter (query)
  conn = connect_ldap(table)
  return conn.search_s(baseDN, ldap.SCOPE_SUBTREE, query)

def insertLDAP(table, dn, entry):
  # Insert a new entry
  # Replace 'cn=jsmith,dc=example,dc=com' with the DN of the new entry
  dnExample = 'cn=jsmith,dc=example,dc=com'
  entryExample = {
      'objectclass': [b'person'],
      'cn': [b'jsmith'],
      'sn': [b'Smith'],
      'mail': [b'jsmith@example.com']
  }
  ldif = modlist.addModlist(entry)
  conn = connect_ldap(table)
  conn.add_s(dn, ldif)

def removeLDAP(table, dn):  
  # Remove an entry
  # Replace 'cn=jsmith,dc=example,dc=com' with the DN of the entry to remove
  dn = 'cn=jsmith,dc=example,dc=com'
  conn = connect_ldap(table)
  conn.delete_s(dn)

def updateLDAP(table, dn, old_entry, new_entry):
  # Update an entry
  # Replace 'cn=jsmith,dc=example,dc=com' with the DN of the entry to update
  dnExample = 'cn=jsmith,dc=example,dc=com'
  old_entryExample = {'mail': [b'jsmith@example.com']}
  new_entryExample = {'mail': [b'john.smith@example.com']}
  ldif = modlist.modifyModlist(old_entry, new_entry)
  conn = connect_ldap(table)
  conn.modify_s(dn, ldif)

def add_user_to_ldap(user):
  # From a LDAP DB
  # https://www.cdata.com/kb/tech/ldap-python-petl.rst
  # Set up the connection
  conn = ldap.initialize('ldap://localhost')  # use your LDAP server address here
  conn.simple_bind_s('cn=admin,dc=example,dc=com', 'password')  # use the admin DN and password

  # Define the user attributes
  attrs = {}
  attrs['objectclass'] = [b'top', b'person']
  attrs['cn'] = [user['first_name'].encode('utf-8')]
  attrs['sn'] = [user['last_name'].encode('utf-8')]
  attrs['uid'] = [user['id'].encode('utf-8')]

  # Convert our dictionary to nice syntax for the add-function using modlist-module
  ldif = ldap.modlist.addModlist(attrs)

  # Do the actual synchronous add-operation to the ldapserver
  conn.add_s('uid=' + user['id'] + ',ou=users,dc=example,dc=com', ldif)

  # Its nice to the server to disconnect and free resources when done
  conn.unbind_s()






def insert(data):  # This function is an example, feel free to adapt it to your needs and your database types
  data = etl.fromdicts([data], header=['id', 'first_name', 'last_name', 'age', 'grade'])
  etl.todb(data, connect_sql(student_table), student_table.tableName, create='False', commit=True)
  # etl.tocsv(data, 'data.csv')
  # etl.tojson(data, 'data.json')
  # insertLDAP(student_ldap, 'cn='+data.firstName+',dc=example,dc=com', {'objectclass': [b'person'], 'cn': [data.firstName], 'sn': [data.lastName], 'mail': [data.email]})
  return JsonResponse({"status": "Successfully inserted"}, status=200)

def insert_all(dataset):
  for data in dataset:  # Could be adapted for sql insertall requests
    insert(data)

def update(id, updated_data):  # This function is an example, feel free to adapt it to your needs and your database types
  whole_sql_table = etl.fromdb(connect_sql(student_table), 'SELECT * FROM students_app_student')
  updated_data = etl.update(whole_sql_table, 'id', id, updated_data)
  etl.todb(table, connect_sql(), 'students_app_student', create='False', commit=True)
  return JsonResponse({"status": "Updated"}, status=200)

def fetch_all(field):
    table = etl.fromdb(connect_sql(), 'SELECT * FROM students_app_student')
    table = etl.sort(table, field)
    return JsonResponse(etl.dicts(table), safe=False)

def fetch(id):
    table = etl.fromdb(connect_sql(), 'SELECT * FROM students_app_student WHERE id = ?', (id,))
    return JsonResponse(etl.dicts(table), safe=False)






import os
import json
import sqlite3
import petl as etl
from django.http import JsonResponse

CSV_PATH = 'students.csv'  # path to your CSV file

def connect_to_db():
    conn = sqlite3.connect('db.sqlite3')
    return conn

def execute(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        if action == 'insert':
            student = data.get('student')
            return insert(student)

        elif action == 'insert_all':
            students = data.get('students')
            return insert_all(students)

        elif action == 'update':
            id = data.get('id')
            student = data.get('student')
            return update(id, student)

        elif action == 'fetch_all':
            field = data.get('field')
            return fetch_all(field)

        elif action == 'fetch':
            id = data.get('id')
            return fetch(id)

        elif action == 'remove':
            id = data.get('id')
            return remove(id)

    else:
        return JsonResponse({"error": "Invalid method"}, status=400)

def insert(student):
    conn = connect_to_db()
    table = etl.fromdicts([student], header=['id', 'first_name', 'last_name', 'age', 'grade'])
    etl.todb(table, conn, 'students_app_student', create='False', commit=True)

    if os.path.exists(CSV_PATH):
        csv_table = etl.fromcsv(CSV_PATH)
        csv_table = etl.cat(csv_table, table)
    else:
        csv_table = table

    etl.tocsv(csv_table, CSV_PATH)
    return JsonResponse({"status": "Inserted"}, status=200)

def insert_all(students):
    conn = connect_to_db()
    table = etl.fromdicts(students, header=['id', 'first_name', 'last_name', 'age', 'grade'])
    etl.todb(table, conn, 'students_app_student', create='False', commit=True)

    if os.path.exists(CSV_PATH):
        csv_table = etl.fromcsv(CSV_PATH)
        csv_table = etl.cat(csv_table, table)
    else:
        csv_table = table

    etl.tocsv(csv_table, CSV_PATH)
    return JsonResponse({"status": "Inserted all"}, status=200)

def update(id, student):
    conn = connect_to_db()
    table = etl.fromdb(conn, 'SELECT * FROM students_app_student')
    table = etl.update(table, 'id', id, student)
    etl.todb(table, conn, 'students_app_student', create='False', commit=True)

    csv_table = etl.fromcsv(CSV_PATH)
    csv_table = etl.update(csv_table, 'id', id, student)
    etl.tocsv(csv_table, CSV_PATH)

    return JsonResponse({"status": "Updated"}, status=200)

def remove(id):
    conn = connect_to_db()
    table = etl.fromdb(conn, 'SELECT * FROM students_app_student WHERE id != ?', (id,))
    etl.todb(table, conn, 'students_app_student', create='False', commit=True)

    csv_table = etl.fromcsv(CSV_PATH)
    csv_table = etl.select(csv_table, lambda rec: rec.id != id)
    etl.tocsv(csv_table, CSV_PATH)

    return JsonResponse({"status": "Removed"}, status=200)

def fetch_all(field):
    conn = connect_to_db()
    table = etl.fromdb(conn, 'SELECT * FROM students_app_student')
    table = etl.sort(table, field)
    return JsonResponse(etl.dicts(table), safe=False)

def fetch(id):
    conn = connect_to_db()
    table = etl.fromdb(conn, 'SELECT * FROM students_app_student WHERE id = ?', (id,))
    return JsonResponse(etl.dicts(table), safe=False)
