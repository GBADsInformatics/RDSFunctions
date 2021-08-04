#
#   Query database tables constructed from FAOSTAT data (from data dump)
#
#   Author: Deb Stacey
#
#   Date of last update: August 3, 2021
#
#   Notes: 
#   1.  This will return one field as:
# python3 queryFAOSTAT.py -t livestock_production_faostat -c China -s Chickens -y 2019 -d population        
#(5246980000,)
#
#   2.  This will return multiple fields as:
# python3 queryFAOSTAT.py -t livestock_production_faostat -c China -s Chickens -y 2019 -d "species, population, year"
#('Chickens', 5246980000, 2019)
#
# This script is returning a dataframe thus the format of the return - I can update this to return data in any required 
# format
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
#    s = species (qspecies)
#    y = year (qyear)
#    d = data field name (dfield_name)
#
def main ( argv ):
    table_name = ""
    qcountry = ""
    qspecies = ""
    qyear = ""
    dfield_name = ""
    try:
        (opts, args) = getopt.getopt ( argv,"ht:c:s:y:d:",["table=","country=","species=","year=","dfield="] )
    except getopt.GetoptError:
        print ( "queryFAOSTAT.py -t <table name> -c <country> -s <species> -y <year> -d <data field name>" )
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ( "queryFAOSTAT.py -t <table name> -c <country> -s <species> -y <year> -d <data field name>" )
            sys.exit()
        elif opt in ("-t", "--table"):
            table_name = arg
        elif opt in ("-c", "--country"):
            qcountry = arg
        elif opt in ("-s", "--species"):
            qspecies = arg
        elif opt in ("-y", "--year"):
            qyear = arg
        elif opt in ("-d", "--dfield"):
            dfield_name = arg
#
# Create connection and cursor    
#
    conn = connect_public()
    cur = conn.cursor()
#
# Select a specific record
#
#    print ( cur.mogrify(f"""SELECT {dfield_name} FROM {table_name} WHERE country='{qcountry}' AND species='{qspecies}' AND year='{qyear}'""") )
    cur.execute(f"""SELECT {dfield_name} FROM {table_name} WHERE country='{qcountry}' AND species='{qspecies}' AND year='{qyear}'""")
    rows = cur.fetchall()
    print ( rows[0] )
#
# Close connection
#
    conn.close()

if __name__ == "__main__":
    main ( sys.argv[1:] )

#
#   End of queryFAOSTAT.py
#
