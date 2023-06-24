def connect_ldap(table):
  # Initialize a connection to the LDAP server
  conn = ldap.initialize(table.databaseUrl)
  # Bind (authenticate) to the server
  # Replace 'cn=admin,dc=example,dc=com' and 'password' with your DN and password
  conn.simple_bind_s(table.dn, table.password)
  return conn


def searchLDAP(table, baseDN, query):
  # Perform a search
  # Replace 'dc=example,dc=com' with your base DN
  # Replace '(objectclass=person)' with your search filter (query)
  conn = connect_ldap(table)
  return conn.search_s(baseDN, ldap.SCOPE_SUBTREE, query)


def insertLDAP(table, dn, entry):
  # Insert a new entry
  # Replace 'cn=jsmith,dc=example,dc=com' with the DN of the new entry
  dnExample = 'cn=jsmith,dc=example,dc=com'
  entryExample = {
      'objectclass': [b'person'],
      'cn': [b'jsmith'],
      'sn': [b'Smith'],
      'mail': [b'jsmith@example.com']
  }
  ldif = modlist.addModlist(entry)
  conn = connect_ldap(table)
  conn.add_s(dn, ldif)


def removeLDAP(table, dn):
  # Remove an entry
  # Replace 'cn=jsmith,dc=example,dc=com' with the DN of the entry to remove
  dn = 'cn=jsmith,dc=example,dc=com'
  conn = connect_ldap(table)
  conn.delete_s(dn)


def updateLDAP(table, dn, old_entry, new_entry):
  # Update an entry
  # Replace 'cn=jsmith,dc=example,dc=com' with the DN of the entry to update
  dnExample = 'cn=jsmith,dc=example,dc=com'
  old_entryExample = {'mail': [b'jsmith@example.com']}
  new_entryExample = {'mail': [b'john.smith@example.com']}
  ldif = modlist.modifyModlist(old_entry, new_entry)
  conn = connect_ldap(table)
  conn.modify_s(dn, ldif)


def add_user_to_ldap(user):
  # From a LDAP DB
  # https://www.cdata.com/kb/tech/ldap-python-petl.rst
  # Set up the connection
  # use your LDAP server address here
  conn = ldap.initialize('ldap://localhost')
  # use the admin DN and password
  conn.simple_bind_s('cn=admin,dc=example,dc=com', 'password')

  # Define the user attributes
  attrs = {}
  attrs['objectclass'] = [b'top', b'person']
  attrs['cn'] = [user['first_name'].encode('utf-8')]
  attrs['sn'] = [user['last_name'].encode('utf-8')]
  attrs['uid'] = [user['id'].encode('utf-8')]

  # Convert our dictionary to nice syntax for the add-function using modlist-module
  ldif = ldap.modlist.addModlist(attrs)

  # Do the actual synchronous add-operation to the ldapserver
  conn.add_s('uid=' + user['id'] + ',ou=users,dc=example,dc=com', ldif)

  # Its nice to the server to disconnect and free resources when done
  conn.unbind_s()
