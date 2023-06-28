from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Student(models.Model):
  ROLES = [
    ('student', 'Student'),
    ('teacher', 'Teacher'),
    ('admin', 'Administration'),
  ]
  GENDER_IN_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Non binary/Other'),
  ]
  gender = models.CharField(max_length=6, choices=GENDER_IN_CHOICES, null=True, blank=True)
  id = models.AutoField(primary_key=True)  # ID is automatically generated
  username = models.CharField(max_length=200)
  first_name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  role = models.CharField(max_length=7, choices=ROLES, default='student')
  age = models.IntegerField()
  grade = models.IntegerField()
  homeaddress = models.CharField(max_length=200)