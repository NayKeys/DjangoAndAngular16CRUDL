"""
  Having vue list with name pointing sql dictionary or csv dictionary or ldap dictionary
  
  Having sql dictionnary with key:vue_name pointing to sql table name -> will be used in the hub.py
"""

VIEW_TREE = {
  "has_view_sets": False,
  "root": {
    "view set 1": {
      "uwu views": {
        "view_1": {
          "method": "sql",
          "table_name": "students_app_student",
          "database_url": "studentsDB.sqlite3",
          "identifier_name": "username",
          "permissions": {
            "student": "_r__",
            "teacher": "_ru_",
            "parent": "<spe>",
            "schooladmin": "crud",
            "admin": "crud",
          }
        },
        "view_2": {
          "method": "sql",
          "table_name": "teachers",
          "database_url": "studentsDB.sqlite3",
          "identifier_name": "username",
          "permissions": {
            "student": "_r__",
            "teacher": "_r__",
            "parent": "____",
            "schooladmin": "_ru_",
            "admin": "crud",
          }
        },
        "view_3": {
          "method": "csv",
          "database_url": "view1.csv",
          "permissions": {
            "student": "_r__",
            "teacher": "_r__",
            "parent": "____",
            "schooladmin": "_r__",
            "admin": "crud",
          }
        },
      },
    },
    "view set 2": {
      "tests views": {
        "view_1": {
          "method": "sql",
          "table_name": "students_app_student",
          "database_url": "studentsDB.sqlite3",
          "identifier_name": "username",
          "permissions": {
            "student": "<spe>",
            "teacher": "_r__",
            "parent": "____",
            "schooladmin": "crud",
            "admin": "crud",
          }
        },
        "view_2": {
          "method": "sql",
          "table_name": "teachers",
          "database_url": "studentsDB.sqlite3",
          "identifier_name": "username",
          "permissions": {
            "student": "_r__",
            "teacher": "_r__",
            "parent": "_r__",
            "schooladmin": "crud",
            "admin": "crud",
          }
        },
        "view_3": {
          "method": "csv",
          "database_url": "view1.csv",
          "permissions": {
            "student": "_r__",
            "teacher": "_r__",
            "parent": "_r__",
            "schooladmin": "crud",
            "admin": "crud",
          }
        },
        "view_4": {
          "method": "csv",
          "database_url": "view1.csv",
          "permissions": {
            "student": "_r__",
            "teacher": "_r__",
            "parent": "_r__",
            "schooladmin": "crud",
            "admin": "crud",
          }
        },
      },
    }
  }
}