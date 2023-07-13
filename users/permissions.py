

def check_permission_create(user, view_name, data):
  print(f'user with username {user.username} with role {user.role} wants to create element {data} in the view {view_name}')
  if user.can_create[view_name]:
    print(f'User {user.username} with role {user.role} is allowed to create element in view {view_name}')
    return True
  else:
    print(f'User {user.username} with role {user.role} is NOT allowed to create element in view {view_name}')
    return False

def check_permission_update(user, view_name, data):
  print(f'user with username {user.username} with role {user.role} wants to update element {data} in the view {view_name}')
  if user.can_update[view_name]:
    print(f'User {user.username} with role {user.role} is allowed to updated element in view {view_name}')
    return True
  else:
    print(f'User {user.username} with role {user.role} is NOT allowed to updated element in view {view_name}')
    return False

def check_permission_delete(user, view_name, data):
  print(f'user with username {user.username} with role {user.role} wants to delete element {data} in the view {view_name}')
  if user.can_delete[view_name]:
    print(f'User {user.username} with role {user.role} is allowed to delete element in view {view_name}')
    return True
  else:
    print(f'User {user.username} with role {user.role} is NOT allowed to delete element in view {view_name}')
    return False

def check_permission_fetch(user, view_name, data):
  print(f'user with username {user.username} with role {user.role} wants to fetch element {data} in the view {view_name}')
  if user.can_read[view_name]:
    print(f'User {user.username} with role {user.role} is allowed to read element in view {view_name}')
    return True
  else:
    print(f'User {user.username} with role {user.role} is NOT allowed to read element in view {view_name}')
    return False

def check_permission_fetch_all(user, view_name, data):
  print(f'user with username {user.username} with role {user.role} wants to fetch all elements of the view {view_name}')
  if user.can_read[view_name]:
    print(f'User {user.username} with role {user.role} is allowed to read elements in view {view_name}')
    return True
  else:
    print(f'User {user.username} with role {user.role} is NOT allowed to read elements in view {view_name}')
    return False