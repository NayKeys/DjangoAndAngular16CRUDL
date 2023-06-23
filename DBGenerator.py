from faker import Faker
from datetime import date
import sqlite3

fake = Faker()

fake.text()

class Student:
  
  classe = ""
  # birthdate = date()
  lastname = ""
  firstname = ""

connection = sqlite3.connect('studentsDB.sqlite3')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE students_app_student (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        role TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade INTEGER NOT NULL,
        address TEXT NOT NULL
    )
''')  # ID auto incremented

import random
role = ('student', 'teacher', 'admin', 'parent')
for _ in range(100):  # Adjust this number to create as many fake students as you need.
    cursor.execute('''
        INSERT INTO students_app_student (first_name, last_name, role, age, grade, address)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (fake.first_name(), fake.last_name(), random.choice(role), fake.random_int(min=18, max=25), fake.random_int(min=1, max=3), fake.address()))

connection.commit()
connection.close()