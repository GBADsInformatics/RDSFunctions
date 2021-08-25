# 
# Author: Rehan Nagoor & Maxim Brochin
# 
# Last Update: August 25, 2021
# 
# Actions:
# - Creates the Ghana table from the data to for uploading into the database
#
# Libraries
import sys
import getopt
import csv

def main ( argv ):
    try:
        (opts, _) = getopt.getopt ( argv,"h",[] )
    except getopt.GetoptError:
        print ( "createGhanaDBFiles.py" )
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ( "createGhanaDBFiles.py" )
            sys.exit()

# open the input file
    rfile = open("20210824_Census_corrected_rev1_cleaned.csv", "r")
    f = open("test.txt", "w")

    rlist = list(csv.reader(rfile,delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True))
    for row in rlist:
        print(row, file=f)
#--------------CREATE Ghana_IDTable-------------
    wfile = open("Ghana_IDTable.csv", "w")

    for i in range(1, len(rlist)):
        print(rlist[i][1], end="", file=wfile)
        print(";"+rlist[i][0], end="", file=wfile)
        for j in range(2,19):
            print(";"+rlist[i][j], end="", file=wfile)
        print("", file=wfile)

    wfile.close()

#--------------CREATE Ghana_Data-------------
    wfile = open("Ghana_Data.csv", "w")

    for i in range(1, len(rlist)):
        print(rlist[i][1], end="", file=wfile)
        for j in list(range(19, 24)) + list(range(29, 46)):
            if j == 29 and rlist[i][j]!="":
                print(";"+str(float(rlist[i][j].replace(',', ''))), end="", file=wfile)
            else:
                print(";"+rlist[i][j], end="", file=wfile)
        print("", file=wfile)

    wfile.close()

#--------------CREATE Ghana_Workers-------------
    wfile = open("Ghana_Workers.csv", "w")

    for i in range(1, len(rlist)):
        print(rlist[i][1], end="", file=wfile)
        for j in range(24, 29):
            print(";"+rlist[i][j], end="", file=wfile)
        print("", file=wfile)

    wfile.close()

#--------------CREATE ghana_issue_amount--------------
    wfile = open("Ghana_Issue_Amount.csv", "w")

    # Calculate amount of issues per row
    for i in range(1, len(rlist)):
        print(f"""{rlist[i][1]};{len([x for x in rlist[i][46:51] if x != ""])}""", file=wfile)

    wfile.close()

#--------------CREATE Ghana_Issue_Description-------------
    issueList = []

    for i in range(1, len(rlist)):
        for j in range(46, 51):
            if (not rlist[i][j] in issueList) and rlist[i][j] != "":
                issueList.append(rlist[i][j])

    wfile = open("Ghana_Issue_Description.csv", "w")
    for i in range(0, len(issueList)):
        print(str(i+1)+";"+issueList[i], file=wfile)

    wfile.close()

#--------------CREATE ghana_issue_link--------------
    wfile = open("Ghana_Issue_Link.csv", "w")

    # Find issues that match
    for i in range(1, len(rlist)):
        for j in range(46, 51):
            for k in range(len(issueList)):
                if rlist[i][j] != "" and rlist[i][j] == issueList[k]:
                    print(f"""{rlist[i][1]};{k+1};{j-45}""", file=wfile)

    wfile.close()

    rfile.close()

if __name__ == "__main__":
    main ( sys.argv[1:] )

#
# End of createGhanaDBFiles.py
#