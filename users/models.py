from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from users.config import ROLE_PERMISSIONS, USERS
from datahub.pipelines.hub import fetch, ReferenceData

from django.contrib.auth.models import AbstractUser
from django.db import models

class Profile(AbstractUser):
  ROLES = [
      ('student', 'Student'),
      ('teacher', 'Teacher'),
      ('parent', 'Parent'),
      ('schooladmin', 'School Admin'),
      ('admin', 'Admin'),
  ]
  role = models.CharField(max_length=11, choices=ROLES, default='student')
  can_create = models.JSONField(default=dict)
  can_read = models.JSONField(default=dict)
  can_update = models.JSONField(default=dict)
  can_delete = models.JSONField(default=dict)
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
  age = models.IntegerField()
  grade = models.IntegerField()
  homeaddress = models.CharField(max_length=200)
  # Adding related_name options
  groups = models.ManyToManyField(
      'auth.Group',
      verbose_name=('groups'),
      blank=True,
      related_name="profile_groups",  # unique related_name
      help_text=(
          'The groups this user belongs to. A user will get all permissions '
          'granted to each of their groups.'
      ),
      related_query_name="user",
  )
  user_permissions = models.ManyToManyField(
      'auth.Permission',
      verbose_name=('user permissions'),
      blank=True,
      related_name="profile_user_permissions",  # unique related_name
      help_text=('Specific permissions for this user.'),
      related_query_name="user",
  )

def generate_users():
  # Delete any users not in the config file
  for user in Profile.objects.all():
      if user.username not in [user_config['username'] for role_users in USERS.values() for user_config in role_users]:
          user.delete()

  # Update or create each user from the config file
  for role, users_config in USERS.items():
    if role not in ROLE_PERMISSIONS:
      print(f"Error: Role '{role}' in USERS_CONFIG is not defined in ROLE_CONFIG")
      continue

    permissions = ROLE_PERMISSIONS[role]

    for user_config in users_config:
      username = user_config['username']
      data = fetch(ReferenceData(username=username))
      user, created = Profile.objects.update_or_create(
        username=username,
        defaults={
          'first_name': data.reference['first_name'],
          'last_name': data.reference['last_name'],
          'email': data.reference['email'],
          'role': role,
          'can_create': {k: v == 'c' for k, v in permissions.items()},
          'can_read': {k: v == 'r' or v == 'id' for k, v in permissions.items()},
          'can_update': {k: v == 'u' for k, v in permissions.items()},
          'can_delete': {k: v == 'd' for k, v in permissions.items()},
          # add other fields as needed
        }
      )

      # Update relationships for 'id' permissions
      for other_role, permission in permissions.items():
        if permission == 'id':
          other_usernames = user_config.get(other_role, [])
          for other_username in other_usernames:
            try:
              other_user = Profile.objects.get(username=other_username)
              # Update the relationship between 'user' and 'other_user'
              # You'll need to adjust this based on how you're modeling relationships
            except Profile.DoesNotExist:
              print(f"Error: User '{other_username}' does not exist")
