#
#    Drop a table in the public data section of the GBADs database on AWS
#
#    Author: Deb Stacey
#
#    Date of last update: August 3, 2021
#
#    Notes: this will drop a table identified by the table name given on the 
#    command line
#
#    Usage: python3 dropPublicTable.py -t table_2
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
#
def main ( argv ):
    table_name = ""
    if len(sys.argv) < 2:
        print ( "dropPublicTable.py -t <table name>" )
        sys.exit(2)
    try:
        (opts, args) = getopt.getopt ( argv,"ht:",["table="] )
    except getopt.GetoptError:
        print ( "dropPublicTable.py -t <table name>" )
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ( "dropPublicTable.py -t <table name>" )
            sys.exit()
        elif opt in ("-t", "--table"):
            table_name = arg
#
#
# Create connection and cursor    
#
    conn = connect_public()
    cur = conn.cursor()
#
# Drop table
#
    try:
        cur.execute(f"""DROP TABLE {table_name} """)
    except Exception as err:
        print ( "Error - cannot drop table: ", err)
        sys.exit(2)
    conn.commit()
#
# Close connection
#
    conn.close()
#

if __name__ == "__main__":
    main ( sys.argv[1:] )

#
#   End of dropPublicTable.py
#
