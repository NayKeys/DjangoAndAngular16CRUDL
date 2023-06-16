import sqlite3

cacheDB = sqlite3.connect(':memory:')
cursor = cacheDB.cursor()


  # Idée : avoir un type "stucturelle" à passer en plus de chaque argument, pour créer la table et accéder aux donner et tout et tout
  
  
  
def createTable():
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
      id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
      name TEXT,
      age INTERGER
    )
  """)
  cacheDB.commit()

def insert(data):
  cursor.execute("""
    INSERT INTO users(name, age) VALUES(:name, :age)"""
  , data)

def insertAll(data):
  users = []
  users.append(("olivier", 30))
  users.append(("jean-louis", 90))
  cursor.executemany("""
    INSERT INTO users(name, age) VALUES(?, ?)"""
  , users)

def execute(sqlrequest):
  cursor.execute(sqlrequest)
  rows = cursor.fetchall()
  return rows

def update(id, data):
  cursor.execute("""UPDATE users SET age = ? WHERE id = 2""", (31,))


def fetchAll(id):
  cursor.execute("""SELECT id, name, age FROM users""")
  rows = cursor.fetchall()
  for row in rows:
    print('{0} : {1} - {2}'.format(row[0], row[1], row[2]))

def undoLast():
  cacheDB.rollback()

def close():
  cacheDB.close()