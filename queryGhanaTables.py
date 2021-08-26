#
#   Query database tables constructed from Ghana CSV file
#
#   Author: Maxim Brochin
#
#   Date of last update: August 25th, 2021
#
#   Notes: 
#   
#   Use -h to 
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
#    r = region (qregion)
#    z = zone/district (qzone)
#    n = owner name (qowner)
#    f = farm name (qfarm)
#    y = prod. year (qyear)
#    c = culture system (qculture_system)
#    l = technology level (qtech_level)
#    w = water type (qwater_type)
#    o = source of water (qwater_source)
#    s = main species cultured (qspecies_cultured)
#    d = data field name (dfield_name)
#    i = id_auto (qID)
#    
#
# Builds query string from query list
def buildQueryString(queries, queryStr):
    if len(queries) != 0:
        if "WHERE" not in queryStr:
            queryStr += " WHERE "
        for i in range(len(queries)-1):
            if queries[i] != "" and queries[len(queries)-1] != "":
                queryStr += queries[i] + " AND "
            else:
                queryStr += queries[i]
        queryStr += queries[len(queries)-1]
        if queryStr == " WHERE ":
            return ""
    return queryStr

# Cleans any quotes or semi-colons
def sanitizeInput(input):
    return input.replace("'", "").replace('"', "").replace(';', "")

def main ( argv ):
    table_name = ""
    qregion = ""
    qzone = ""
    qowner = ""
    qfarm = ""
    qyear = ""
    qculture_system = ""
    qtech_level = ""
    qwater_type = ""
    qwater_source = ""
    qspecies_cultured = ""
    qissue_code = ""
    qissue_num = ""
    dfield_name = "*"
    qID = ""
    try:
        (opts, args) = getopt.getopt ( argv,"ht:r:z:n:f:y:c:l:w:o:s:a:b:d:i:",["table=","region=","zone=","owner=","farm=","year=","culture=","tech=","water=","waterSource=","species=","issueCode=","issueNum=","dfield=","id="] )
    except getopt.GetoptError:
        print ( "queryGhanaTables.py -t <table name> -r <region> -z <zone> -n <owner> -f <farm> -y <year> -c <culture system> -l <tech level> -w <water type> -o <water source> -s <species> -a <issueCode> -b <issueNum> -d <data field name> -i <id_auto>" )
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ( "queryGhanaTables.py -t <table name> -r <region> -z <zone> -n <owner> -f <farm> -y <year> -c <culture system> -l <tech level> -w <water type> -o <water source> -s <species> -a <issueCode> -b <issueNum> -d <data field name> -i <id_auto>\n" )
            print("t = table name (table_name)\nr = region (qregion)\nz = zone/district (qzone)\nn = owner name (qowner)\nf = farm name <qfarm>\ny = prod. year (qyear)\nc = culture system (qculture_system)\n"+
            "l = technology level (qtech_level)\nw = water type (qwater_type)\no = source of water (qwater_source)\ns = main species cultured (qspecies_cultured)"+
            "\na = issue code (qissue_code)\nb = issue num (qissue_num)\nd = data field name (dfield_name)\ni = id_auto (qID)")
            sys.exit()
        elif opt in ("-t", "--table"):
            table_name = sanitizeInput(arg)
        elif opt in ("-r", "--region"):
            qregion = sanitizeInput(arg)
        elif opt in ("-z", "--zone"):
            qzone = sanitizeInput(arg)
        elif opt in ("-n", "--owner"):
            qowner = sanitizeInput(arg)
        elif opt in ("-f", "--farm"):
            qfarm = sanitizeInput(arg)
        elif opt in ("-y", "--year"):
            qyear = sanitizeInput(arg)
        elif opt in ("-c", "--culture"):
            qculture_system = sanitizeInput(arg)
        elif opt in ("-l", "--tech"):
            qtech_level = sanitizeInput(arg)
        elif opt in ("-w", "--water"):
            qwater_type = sanitizeInput(arg)
        elif opt in ("-o", "--waterSource"):
            qwater_source = sanitizeInput(arg)
        elif opt in ("-s", "--species"):
            qspecies_cultured = sanitizeInput(arg)
        elif opt in ("-a", "--issueCode"):
            qissue_code = sanitizeInput(arg)
        elif opt in ("-b", "--issueNum"):
            qissue_num = sanitizeInput(arg)
        elif opt in ("-d", "--dfield"):
            dfield_name = sanitizeInput(arg)
        elif opt in ("-i", "--id"):
            qID = sanitizeInput(arg)
#
# Create connection and cursor    
#
    conn = connect_public()
    cur = conn.cursor()

# Select an id and check which params are used to build query string
    queries = []
    if qregion:
        queries.append(f"""ghana_idtable.region='{qregion}'""")
    if qzone:
        queries.append(f"""ghana_idtable.district='{qzone}'""")
    if qowner:
        queries.append(f"""ghana_idtable.owner_name='{qowner}'""")
    if qfarm:
        queries.append(f"""ghana_idtable.farm_name='{qfarm}'""")
    if qID:
        queries.append(f"""ghana_idtable.id_auto='{qID}'""")
    idQuery = buildQueryString(queries, "")

# Check which table is used and perform query based on table used
    if table_name == "ghana_data":
        queries = []
        if qyear:
            queries.append(f"""ghana_data.prod_year='{qyear}'""")
        if qculture_system:
            queries.append(f"""ghana_data.culture_system='{qculture_system}'""")
        if qtech_level:
            queries.append(f"""ghana_data.technology_level='{qtech_level}'""")
        if qwater_type:
            queries.append(f"""ghana_data.water_type='{qwater_type}'""")
        if qwater_source:
            queries.append(f"""ghana_data.water_source='{qwater_source}'""")
        if qspecies_cultured:
            queries.append(f"""ghana_data.main_species_cultured='{qspecies_cultured}'""")
        dataQuery = buildQueryString(queries, "").replace(" WHERE ", "")
        print(f"""SELECT {table_name}.{dfield_name} from ghana_idtable INNER JOIN {table_name} USING(id_auto){buildQueryString([idQuery.replace(" WHERE ", ""), dataQuery], "")}\n""")
        cur.execute(f"""SELECT {table_name}.{dfield_name} from ghana_idtable INNER JOIN {table_name} USING(id_auto){buildQueryString([idQuery.replace(" WHERE ", ""), dataQuery], "")}""")
        pass
    elif table_name == "ghana_workers" or table_name == "ghana_issue_amount":
        print(f"""SELECT {table_name}.{dfield_name} from ghana_idtable INNER JOIN {table_name} USING(id_auto){idQuery}\n""")
        cur.execute(f"""SELECT {table_name}.{dfield_name} from ghana_idtable INNER JOIN {table_name} USING(id_auto){idQuery}""")
        pass
    elif table_name == "ghana_issue_description":
        queries = []
        if qissue_code:
            queries.append(f"""{table_name}.issue_code='{qissue_code}'""")
        if qissue_num:
            queries.append(f"""ghana_issue_link.issue_num='{qissue_num}'""")
        issueQuery = buildQueryString(queries, "").replace(" WHERE ", "")
        print(f"""SELECT ghana_issue_link.id_auto,ghana_issue_link.issue_num,{table_name}.* from ghana_idtable INNER JOIN ghana_issue_link USING(id_auto) INNER JOIN {table_name} ON ghana_issue_link.issue_code={table_name}.issue_code{buildQueryString([idQuery.replace(" WHERE ", ""), issueQuery], "")}\n""")
        cur.execute(f"""SELECT ghana_issue_link.id_auto,ghana_issue_link.issue_num,{table_name}.* from ghana_idtable INNER JOIN ghana_issue_link USING(id_auto) INNER JOIN {table_name} ON ghana_issue_link.issue_code={table_name}.issue_code{buildQueryString([idQuery.replace(" WHERE ", ""), issueQuery], "")}""")
    else:
        print("Error: table name needs to be entered or forbidden from accessing personal data.")

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
#   End of queryGhanaTables.py
#