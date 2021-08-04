#
#    Create a table in the public data section of the GBADs database on AWS
#
#    Author: Deb Stacey
#
#    Date of last update: August 3, 2021
#
#    Notes: this will create a table from a table name given on the command line
#    and a file that contains the schema.  There is an example schema file named
#    "schema_example" to show what the schema description should look like.
#
#    Usage: python3 createPublicTable.py -t table_example1 -s schema_example
#
# Libraries
import os
import sys
import getopt
import psycopg2 as ps
from secure_connect import connect_public
#
# Get parameters from the command line
#    t = table name (table_name)
#    s = schema file name (schema_name)
#
def main ( argv ):
    table_name = ""
    if len(sys.argv) < 3:
        print ( "createPublicTable.py -t <table name> -s <schema file name>" )
        sys.exit(2)
    try:
        (opts, args) = getopt.getopt ( argv,"ht:s:",["table=","schema="] )
    except getopt.GetoptError:
        print ( "createPublicTable.py -t <table name> -s <schema file name" )
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ( "createPublicTable.py -t <table name> -s <schema file name" )
            sys.exit()
        elif opt in ("-t", "--table"):
            table_name = arg
        elif opt in ("-s", "--schema"):
            schema_name = arg
#
# Create connection and cursor    
#
    conn = connect_public()
    cur = conn.cursor()
#
# Check what is in the database: get a list of tables
# 
    cur.execute("SELECT table_schema,table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_schema,table_name ;")
    tables = cur.fetchall()
    print ( "There are "+str(len(tables))+" table(s) in the Public Data Section" )
    index = 1
    for table in tables:
        print( str(index)+".  "+table[1])
        index = index + 1
#
# Create the schema from a file
#
    sInput = open (schema_name, "r")
    schema = sInput.read()
    sInput.close()
#
# Create a table
#
    cur.execute(f"""CREATE TABLE {table_name} ( {schema} );""")
    conn.commit()
#
# Again Check what is in the database: get a list of tables
# 
    cur.execute("SELECT table_schema,table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_schema,table_name ;")
    tables = cur.fetchall()
    print ( "Now there are ",len(tables)," table(s) in the database: " )
    for table in tables:
        print(table)
#
#
# Close connection
    conn.close()

if __name__ == "__main__":
    main ( sys.argv[1:] )

#
#   End of dropPublicTable.py
#

