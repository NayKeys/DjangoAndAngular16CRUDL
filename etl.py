import petl as etl

# From a SQL DB
# https://www.cdata.com/kb/tech/csv-python-petl.rst
table1 = etl.fromdb('postgresql://postgres:postgres@localhost:5432/postgres', 'SELECT * FROM mytable')

# From a LDAP DB
# https://www.cdata.com/kb/tech/ldap-python-petl.rst

#From a CSV file
table3 = etl.fromcsv('data.csv')

# From a JSON file
table4 = etl.fromjson('data.json')