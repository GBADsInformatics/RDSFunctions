#
#   Query database tables constructed from Ethiopia CSA Report data
#
#   Author: Maxim Brochin
#
#   Date of last update: August 12, 2021
#
#   Notes: 
#   1.  python3 queryTables.py -t <table name> -c Ethiopia 
#       Will return all records with Ethiopia from a table
#
#   2.  python3 queryTables.py -t <table name> -s "Ethiopia CSA Livestock PDFs"
#       Will return all records from the datasource of a table
#
#   3.  python3 queryTables.py -t <table name> -r Tigray
#       Will return all records of the region Tigray from a table
#
#   4.  python3 queryTables.py -t <table name> -z "North Tigray"
#       Will return all records of the zone North Tigray from a table
#
#   5.  python3 queryTables.py -t <table name> -y 2020
#       Will return all records from 2020 of a table
#
#   6.  python3 queryTables.py -t <table name> -d <data field name>
#       Will return all records from a specific data field of a table
#
#   7.  python3 queryTables.py -t <table name> -z Tigray
#       When getting data of the region itself, put the name of the region for the zone argument
#
#   8.  python3 queryTables.py -t cattle_dairy -r Tigray -z "North Tigray" -y 2020 -d "dairy_cows"
#       This example finds the ID for record containing Tigray and North Tigray, gets the record for 2020
#       in cattle_dairy and returns the column for dairy_cows 
#
# Libraries
import os
import sys
import getopt
import psycopg2 as ps
import pandas as pd
from secure_connect import connect_public
#
# Get parameters from the command line
#    t = table name (table_name)
#    c = country (qcountry)
#    r = region (qregion)
#    z = zone (qzone)
#    y = year (qyear)
#    d = data field name (dfield_name)
#    s = datasource (qdatasource)
#
# Builds query string from query list
def buildQueryString(queries, queryStr):
    if len(queries) != 0:
        if "WHERE" not in queryStr:
            queryStr += " WHERE "
        for i in range(len(queries)-1):
            queryStr += queries[i] + " AND "
        queryStr += queries[len(queries)-1]
    return queryStr
    

def main ( argv ):
    table_name = ""
    qcountry = ""
    qregion = ""
    qzone = ""
    qyear = ""
    dfield_name = ""
    qdatasource = ""
    try:
        (opts, args) = getopt.getopt ( argv,"ht:c:r:z:y:d:s:",["table=","country=","region=","zone=","year=","dfield=","datasource="] )
    except getopt.GetoptError:
        print ( "queryTables.py -t <table name> -c <country> -r <region> -z <zone> -y <year> -d <data field name> -s <datasource>" )
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ( "queryTables.py -t <table name> -c <country> -r <region> -z <zone> -y <year> -d <data field name> -s <datasource>" )
            sys.exit()
        elif opt in ("-t", "--table"):
            table_name = arg
        elif opt in ("-c", "--country"):
            qcountry = arg
        elif opt in ("-r", "--region"):
            qregion = arg
        elif opt in ("-z", "--zone"):
            qzone = arg
        elif opt in ("-y", "--year"):
            qyear = arg
        elif opt in ("-d", "--dfield"):
            dfield_name = arg
        elif opt in ("-s", "--datasource"):
            qdatasource = arg
#
# Create connection and cursor    
#
    conn = connect_public()
    cur = conn.cursor()

# Select an id and check which params are used to build query string
    queries = []
    if qcountry:
        queries.append(f"""country='{qcountry}'""")
    if qregion:
        queries.append(f"""region='{qregion}'""")
    if qzone:
        queries.append(f"""zone='{qzone}'""")
    if qdatasource:
        queries.append(f"""datasource='{qdatasource}'""")
    queryStr = buildQueryString(queries, "SELECT id from idtable")

# Select queries and check which params are used to build query string
    queries = []
    if qyear:
        queries.append(f""" AND year='{qyear}'""")
    if table_name and dfield_name:
        cur.execute(buildQueryString(queries, f"""SELECT {dfield_name} FROM {table_name} WHERE id IN ({queryStr})"""))
    elif table_name:
        cur.execute(buildQueryString(queries, f"""SELECT * FROM {table_name} WHERE id IN ({queryStr})"""))
    else:
        print("Error: table name needs to be entered.")

# Try to print records found
    try:
        rows = cur.fetchall()
        print ( rows )
    except:
        print("No records were found.")
#
# Close connection
#
    conn.close()

if __name__ == "__main__":
    main ( sys.argv[1:] )

#
#   End of query.py
#