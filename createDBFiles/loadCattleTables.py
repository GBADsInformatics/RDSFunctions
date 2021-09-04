#
#   Creating and Loading the Production-Livestock (Population) data from FAOSTAT (from data dump)
#   Data is in a CSV file
#
#   Author: Deb Stacey, Rehan Nagoor
#
#   Date of last update: August 6, 2021
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
#--------------------ADDING cattle_category FILES--------------------
#
#clear anything already in the table
# cur.execute("""DELETE FROM cattle_category;""")
# # Insert data from the CSV files into the table
# print ( "\nadding data to cattle_category" )
# years = ["2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020"]
# for year in years:
#     with open(year+"_cattle_category.csv", 'r') as row:
#         cur.copy_from(row, 'cattle_category', sep=',')
#         print(year+" files added")
# #
# # Commit data insertion
#     conn.commit()
# #
# #--------------------ADDING cattle_usage FILES--------------------
# #
# #clear anything already in the tables
# cur.execute("""DELETE FROM cattle_usage;""")
# # Insert data from the CSV files into the table
# print ( "\nadding data to cattle_usage" )
# for year in years:
#     with open(year+"_cattle_usage.csv", 'r') as row:
#         cur.copy_from(row, 'cattle_usage', sep=',')
#         print(year+" files added")
# #
# # Commit data insertion
#     conn.commit()
# #
# #--------------------ADDING cattle_health FILES--------------------
# #
# #clear anything already in the table
# cur.execute("""DELETE FROM cattle_health;""")
# # Insert data from the CSV files into the table
# print ( "\nadding data to cattle_health" )
# for year in years:
#     with open(year+"_cattle_health.csv", 'r') as row:
#         cur.copy_from(row, 'cattle_health', sep=',')
#         print(year+" files added")
# #
# # Commit data insertion
#     conn.commit()
# #
# #--------------------ADDING cattle_dairy FILES--------------------
# #
# #clear anything already in the table
# cur.execute("""DELETE FROM cattle_dairy;""")
# # Insert data from the CSV files into the table
# print ( "\nadding data to cattle_dairy" )
# for year in years:
#     with open(year+"_cattle_dairy.csv", 'r') as row:
#         cur.copy_from(row, 'cattle_dairy', sep=',')
#         print(year+" files added")
# #
# # Commit data insertion
#     conn.commit()
# #
# #--------------------ADDING cattle_holdings FILES--------------------
# #
# #clear anything already in the table
# cur.execute("""DELETE FROM cattle_holdings;""")
# # Insert data from the CSV files into the table
# print ( "\nadding data to cattle_holdings" )
# years.remove("2003")
# for year in years:
#     with open(year+"_cattle_holdings.csv", 'r') as row:
#         cur.copy_from(row, 'cattle_holdings', sep=',')
#         print(year+" files added")
# #
# # Commit data insertion
#     conn.commit()
# #
# #--------------------ADDING cattle_estimation FILES--------------------
# #
# #clear anything already in the table
# cur.execute("""DELETE FROM cattle_estimation;""")
# # Insert data from the CSV files into the table
# print ( "\nadding data to cattle_estimation" )
# years.remove("2004")
# for year in years:
#     with open(year+"_cattle_estimation.csv", 'r') as row:
#         cur.copy_from(row, 'cattle_estimation', sep=',')
#         print(year+" files added")
# #
# # Commit data insertion
#     conn.commit()
#
# Close connection
conn.close()
print ( "Connection to gbadske-database-public-data closed" )
#
#  End of loadCattleTables.py
#
