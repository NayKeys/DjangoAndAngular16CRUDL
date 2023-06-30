from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from users.config import ROLE_PERMISSIONS, USERS

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
  # gender = models.CharField(max_length=6, choices=GENDER_IN_CHOICES, null=True, blank=True)
  # ID = models.AutoField(primary_key=True)  # ID is automatically generated
  # username = models.CharField(max_length=200)
  # first_name = models.CharField(max_length=200)
  # last_name = models.CharField(max_length=200)
  # age = models.IntegerField()
  # grade = models.IntegerField()
  # homeaddress = models.CharField(max_length=200)
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
    if user.username not in [user_config['username'] for user_in_role in USERS.values() for user_config in user_in_role]:  # Listing every username for every users by role in USERS list of roles
      user.delete()
  # Update or create each user from the config file
  for role_name, users_in_role in USERS.items():
    if role_name not in ROLE_PERMISSIONS:
      print(f"Error: Role '{role_name}' in USERS is not defined in ROLE_PERMISSIONS")
      continue
    view_permissions_of_role = ROLE_PERMISSIONS[role_name]
    # Updating users in ORM
    for user_config in users_in_role:  # User are listed by role
      username = user_config['username']
      user2, created = Profile.objects.update_or_create(
        username=username,
        defaults={
          'role': role_name,
          'can_create': {view_name: ('c' in view_rights) for view_name, view_rights in view_permissions_of_role.items()},  # Creates a dictionnary of booleans for creation rights of the different views, key: view name (each key of view_permissions_of_role), value: boolean (True if the user has the right to create, False otherwise)
          'can_read': {view_name: ('r' in view_rights) for view_name, view_rights in view_permissions_of_role.items()},
          'can_update': {view_name: ('u' in view_rights) for view_name, view_rights in view_permissions_of_role.items()},
          'can_delete': {view_name: ('d' in view_rights) for view_name, view_rights in view_permissions_of_role.items()},
          # add other fields as needed
        }
      )

      # Update relationships for '<spe>' permissions
      # for view_name, view_rights in view_permissions_of_role.items():
      #   if view_rights == '<spe>':
      #     ids = user_config.get(view_name, [])
      #     if len(ids) == 0:
      #       print(f"Role '{role_name}' has right '<spe>' on view '{view_name}' but user '{user_config['username']}' doesn't list any specific element ids with that view name")
      #     else:
      #       user, created = Profile.objects.update(
      #         username=username,
      #         defaults={
      #           view_name: [element_id for element_id in ids]
      #         }
      #       )
            # Update the relationship between 'user' and 'other_user'
            # You'll need to adjust this based on how you're modeling relationships
