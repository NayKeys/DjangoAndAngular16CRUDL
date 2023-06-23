from django.db import models

# Create your models here.

class Student(models.Model):
  id = models.AutoField(primary_key=True)  # ID is automatically generated
  first_name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  role = models.CharField(max_length=200)
  age = models.IntegerField()
  grade = models.IntegerField()
  address = models.CharField(max_length=200)