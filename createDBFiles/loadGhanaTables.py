#
#   Creating and Loading the ghana data (from data dump) Data is in a CSV file
#
#   Author: Deb Stacey, Rehan Nagoor
#
#   Date of last update: August 25, 2021
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
#--------------------ADDING ghana_idtable FILE--------------------
#
#clear anything already in the tables
cur.execute("""DELETE FROM ghana_workers;""")
cur.execute("""DELETE FROM ghana_data;""")
cur.execute("""DELETE FROM ghana_idtable;""")
cur.execute("""DELETE FROM ghana_issue_description;""")
cur.execute("""DELETE FROM ghana_issue_link;""")
cur.execute("""DELETE FROM ghana_issue_amount;""")

# Insert data from the CSV files into the table
print ( "adding data to ghana_idtable" )
with open("Ghana_IDTable.csv", 'r') as row:
    cur.copy_from(row, 'ghana_idtable', sep=';', null="")
    print("ghana_idtable data added")
#
# Commit data insertion
    conn.commit()
#
# check that the data has been added
# cur.execute("""SELECT * FROM idtable;""")
# rows = cur.fetchall()
# if len(rows) > 0:
#     print ( rows )
# else:
#     print ( "Empty" )
#
#--------------------ADDING ghana_data FILES--------------------
#
# Insert data from the CSV files into the table
print ( "\nadding data to ghana_data" )
with open("Ghana_Data.csv", 'r') as row:
    cur.copy_from(row, 'ghana_data', sep=';', null="")
    print("ghana_data data added")
#
# Commit data insertion
    conn.commit()
#
#--------------------ADDING ghana_workers FILES--------------------
#
# Insert data from the CSV files into the table
print ( "\nadding data to ghana_workers" )
with open("Ghana_Workers.csv", 'r') as row:
    cur.copy_from(row, 'ghana_workers', sep=';', null="")
    print("ghana_workers data added")
#
# Commit data insertion
    conn.commit()
#
#--------------------ADDING ghana_issue_description FILES--------------------
#
# Insert data from the CSV files into the table
print ( "\nadding data to ghana_issue_description" )
with open("Ghana_Issue_Description.csv", 'r') as row:
    cur.copy_from(row, 'ghana_issue_description', sep=';', null="")
    print("ghana_issue_description data added")
#
# Commit data insertion
    conn.commit()
#
#--------------------ADDING ghana_issue_link FILES--------------------
#
# Insert data from the CSV files into the table
print ( "\nadding data to ghana_issue_link" )
with open("Ghana_Issue_Link.csv", 'r') as row:
    cur.copy_from(row, 'ghana_issue_link', sep=';', null="")
    print("ghana_issue_link data added")
#
# Commit data insertion
    conn.commit()
#
#--------------------ADDING ghana_issue_amount FILES--------------------
#
# Insert data from the CSV files into the table
print ( "\nadding data to ghana_issue_amount" )
with open("Ghana_Issue_Amount.csv", 'r') as row:
    cur.copy_from(row, 'ghana_issue_amount', sep=';', null="")
    print("ghana_issue_amount data added")
#
# Commit data insertion
    conn.commit()
#
# Close connection
conn.close()
print ( "Connection to gbadske-database-public-data closed" )
#
#  End of loadGhanaTables.py
#
