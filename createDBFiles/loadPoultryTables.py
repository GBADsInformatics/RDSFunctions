#
#   Creating and Loading the poultry data (from data dump) Data is in a CSV file
#
#   Author: Deb Stacey, Rehan Nagoor
#
#   Date of last update: August 20, 2021
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
#--------------------ADDING idtable FILE--------------------
#
#clear anything already in the table
cur.execute("""DELETE FROM idtable;""")
# Insert data from the CSV files into the table
print ( "adding data to idtable" )
with open("IDTable.csv", 'r') as row:
    cur.copy_from(row, 'idtable', sep=',')
    print("idtable data added")
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
#--------------------ADDING poultry_inventory FILES--------------------
#
#clear anything already in the table
cur.execute("""DELETE FROM poultry_inventory;""")
# Insert data from the CSV files into the table
print ( "\nadding data to poultry_inventory" )
years = ["2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020"]
for year in years:
    with open(year+"_poultry_inventory.csv", 'r') as row:
        cur.copy_from(row, 'poultry_inventory', sep=',')
        print(year+" files added")
#
# Commit data insertion
    conn.commit()
#
#--------------------ADDING poultry_health FILES--------------------
#
#clear anything already in the tables
cur.execute("""DELETE FROM poultry_health;""")
# Insert data from the CSV files into the table
print ( "\nadding data to poultry_health" )
for year in years:
    with open(year+"_poultry_health.csv", 'r') as row:
        cur.copy_from(row, 'poultry_health', sep=',')
        print(year+" files added")
#
# Commit data insertion
    conn.commit()
#
#--------------------ADDING poultry_eggs FILES--------------------
#
#clear anything already in the table
cur.execute("""DELETE FROM poultry_eggs;""")
# Insert data from the CSV files into the table
print ( "\nadding data to poultry_eggs" )
years.remove("2003")
for year in years:
    with open(year+"_poultry_eggs.csv", 'r') as row:
        cur.copy_from(row, 'poultry_eggs', sep=',')
        print(year+" files added")
#
# Commit data insertion
    conn.commit()
#
#--------------------ADDING poultry_holdings FILES--------------------
#
#clear anything already in the table
cur.execute("""DELETE FROM poultry_holdings;""")
# Insert data from the CSV files into the table
print ( "\nadding data to poultry_holdings" )
for year in years:
    with open(year+"_poultry_holdings.csv", 'r') as row:
        cur.copy_from(row, 'poultry_holdings', sep=',')
        print(year+" files added")
#
# Commit data insertion
    conn.commit()
#
#--------------------ADDING poultry_estimation FILES--------------------
#
#clear anything already in the table
cur.execute("""DELETE FROM poultry_estimation;""")
# Insert data from the CSV files into the table
print ( "\nadding data to poultry_estimation" )
years.remove("2004")
for year in years:
    with open(year+"_poultry_estimation.csv", 'r') as row:
        cur.copy_from(row, 'poultry_estimation', sep=',')
        print(year+" files added")
#
# Commit data insertion
    conn.commit()
#
# Close connection
conn.close()
print ( "Connection to gbadske-database-public-data closed" )
#
#  End of loadCattleTables.py
#
