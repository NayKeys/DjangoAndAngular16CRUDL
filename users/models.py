from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from users.config import USERS
from datahub.config import VIEW_TREE

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

def flatten_view_tree(node, path=""):
  flat_views = {}
  for key, value in node.items():
    new_path = f"{path} > {key}"
    if "permissions" in value:
      # This node is a view, add it to the flat_views
      flat_views[new_path] = value["permissions"]
    else:
      # This node is not a view, recurse into it
      flat_views.update(flatten_view_tree(value, new_path))
  return flat_views

def generate_users():
  flat_views = flatten_view_tree(VIEW_TREE["root"])
  
  # Delete any users not in the config file
  for user in Profile.objects.all():
    if user.username not in [user_config['username'] for user_in_role in USERS.values() for user_config in user_in_role]:  # Listing every username for every users by role in USERS list of roles
      user.delete()

  # Update or create each user from the config file
  for role_name, users_in_role in USERS.items():
    for user_config in users_in_role:
      username = user_config['username']
      user2, created = Profile.objects.update_or_create(
        username=username,
        defaults={
            'role': role_name,
        }
      )
      # Updating permissions for each view
      for view_name, view_permissions in flat_views.items():
        user2.can_create[view_name] = ('c' in view_permissions.get(role_name, ""))# Creates a dictionnary of booleans for creation rights of the different views, key: view name (each key of view_permissions_of_role), value: boolean (True if the user has the right to create, False otherwise)
        user2.can_read[view_name] = ('r' in view_permissions.get(role_name, ""))
        user2.can_update[view_name] = ('u' in view_permissions.get(role_name, ""))
        user2.can_delete[view_name] = ('d' in view_permissions.get(role_name, ""))
      
      # Save the changes to the user object
      user2.save()
      print(f"User '{username}' has been created or updated with role '{role_name}'")
      
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
