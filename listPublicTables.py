#
#    List all the tables currently in the public data section of the GBADs database on AWS
#
#    Author: Deb Stacey
#
#    Date of last update: August 3, 2021
#
#    Usage: python3 listPublicTables.py
#
# Libraries
import psycopg2 as ps
from secure_connect import connect_public
#
# Create connection and cursor    
conn = connect_public()
cur = conn.cursor()
#
# Check what is in the database: get a list of tables
# 
cur.execute("SELECT table_schema,table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_schema,table_name ;")
tables = cur.fetchall()
if len(tables) == 1:
    print ( "There is "+str(len(tables))+" table in the Public Data Section" )
else:
    print ( "There are "+str(len(tables))+" tables in the Public Data Section" )
index = 1
for table in tables:
    print( str(index)+".  "+table[1])
    index = index + 1
#
# Close connection
#
conn.close()
