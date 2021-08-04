#
#   Creating and Loading the Production-Livestock (Population) data from FAOSTAT (from data dump)
#   Data is in a CSV file
#
#   Author: Deb Stacey
#
#   Date of last update: August 3, 2021
#
#   Notes: the CSV file uses the semi-colon (;) to separate fields because there seemed to be a
#   problem because one of the fields uses a comma (,) as part of its data and that did not seem
#   to work with copy_from (psycopg2) - this might be correctable but I chose to change the separator
#   and it does work with the comma as long as the fields do not contain a comma (even with quotes
#   around the field).
#   The CSV file also does not put quotes around the data in the fields since there are no semi-colons
#   in the data and putting in quotes also seemed to add them to the database field which was not 
#   desirable particularly when forming queries.
#   And obviously there are no parameters and no error checking (!) - please update as desired
#
#   Libraries
#
import psycopg2 as ps
from secure_connect import connect_public
#
# Create connection and cursor    
print ( "connecting to gbadske-database-public-data..." )
#
#  Connection parameters include:
#     host = database location in AWS which is gbadske-database-public-data.cp73fx22weet.ca-central-1.rds.amazonaws.com
#     dbname = name of the database which is publicData_1 since this database will contain public data
#     user = main database user (and currently the only database user) which is the default user "postgres"
#     password = password for the database user - obviously this is a problem for security and we will have to change this to read
#     from a file that contains the password and/or restrict the distribution of the database scripts
#
conn = connect_public()
cur = conn.cursor()
print ( "connection to gbadske-database-public-data complete" )
#
# Create a table a livestock production ("stocks") data from FAOSTAT
#
cur.execute("""CREATE TABLE livestock_production_faostat
                (Country varchar(80),
                Species varchar(30),
                Year integer,
                Population bigint, 
                Flag varchar(5))""")
#
# Commit table creation
#
conn.commit()
print ( "Table livestock_production_faostat created" )
#
# Insert data from CSV file into the table
with open('livestock_production_faostat.csv', 'r') as row:
    next(row)    # Skip the header row
    cur.copy_from(row, 'livestock_production_faostat', sep=';')
#
# Commit data insertion
conn.commit()
#
# check that the data has been added
cur.execute("""SELECT * FROM livestock_production_faostat;""")
rows = cur.fetchall()
if len(rows) > 0:
    print ( rows )
else:
    print ( "Empty" )
#
# Close connection
conn.close()
print ( "Connection to gbadske-database-public-data closed" )
#
#  End of loadTable.py
#
