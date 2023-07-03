"""
  Having vue list with name pointing sql dictionary or csv dictionary or ldap dictionary
  
  Having sql dictionnary with key:vue_name pointing to sql table name -> will be used in the hub.py
"""

VIEW_LIST = [
  {
    "vue_name": "sql_view_1",
    "method": "sql",
    "table_name": "students_app_student",
    "database_url": "studentsDB.sqlite3",
    "identifier_name": "id",
  },
  {
    "vue_name": "sql_view_2",
    "method": "sql",
    "table_name": "students_app_student",
    "database_url": "studentsDB.sqlite3",
    "identifier_name": "id",
  },
  {
    "vue_name": "view3",
    "method": "csv",
    "database_url": "view1.csv",
  },
]