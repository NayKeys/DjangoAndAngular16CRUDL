from django.db import models

# Create your models here.

class Student(models.Model):
  ROLES = [
    ('student', 'Student'),
    ('teacher', 'Teacher'),
    ('admin', 'Administration'),
  ]
  id = models.AutoField(primary_key=True)  # ID is automatically generated
  first_name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  role = models.CharField(max_length=7, choices=ROLES, default='student')
  age = models.IntegerField()
  grade = models.IntegerField()
  address = models.CharField(max_length=200)