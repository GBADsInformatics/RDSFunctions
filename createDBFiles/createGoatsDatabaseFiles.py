# 
# Author: Rehan Nagoor & Maxim Brochin
# 
# Last Update: August 31, 2021
# 
# Actions:
# - creates the appropriate Goats files to upload into the database 
#
# Libraries
import sys
import getopt
import csv
from nameVariants import variantDict

# Get's the ID from name
def getId(idDict, cols):
    # If region
    if cols[1] == '':
        # Use special case for Oromia region
        if cols[0] == "Oromia" or cols[0] == "Oromiya":
            return idDict[cols[0]+" Region"]
        else:
            return idDict[cols[0]]
    # If zone
    else:
        # Use special case for Amhara's Oromia zone
        if cols[0] == "Amhara" and (cols[0]+" "+cols[1] in variantDict["Amhara Oromia"] or cols[0]+" "+cols[1] == "Amhara Oromia"):
            return idDict[cols[0]+" "+cols[1]]
        else:
            return idDict[cols[1]]

def main ( argv ):
    try:
        (opts, _) = getopt.getopt ( argv,"h",[] )
    except getopt.GetoptError:
        print ( "createGoatsDatabaseFiles.py" )
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ( "createGoatsDatabaseFiles.py" )
            sys.exit()

#--------------CREATE idtable along with id dictionary--------------
    idFile = open("IDTable.csv", "w")
    idDict = {}
    regionDict = {}
    idNum = 0
    startYear,endYear = 2003,2021
    for y in range(startYear, endYear):
        nameFile = open(f"""{y}_Table_3-1.csv""", "r")
        names = list(csv.reader(nameFile, delimiter=","))
        for i in range(1, len(names)):
            # Add if region entry
            if names[i][1] == '' and names[i][0] not in idDict:
                # If Oromia region is used, add special case
                if names[i][0]+" Region" == "Oromia Region" and "Oromia Region" not in idDict and names[i][0] != "Oromiya":
                    idDict[names[i][0]+" Region"] = idNum
                    regionDict[idNum] = names[i][0]
                    for variant in variantDict[names[i][0]+" Region"]:
                        idDict[variant] = idNum
                else:
                    idDict[names[i][0]] = idNum
                    regionDict[idNum] = names[i][0]
                    # If variants exist, add them
                    if names[i][0] in variantDict:
                        for variant in variantDict[names[i][0]]:
                            idDict[variant] = idNum
                idNum += 1
            # Add if zone entry
            elif names[i][1] not in idDict:
                # If Amhara's Oromia zone is used, add special case
                if names[i][0]+" "+names[i][1] == "Amhara Oromia" and "Amhara Oromia" not in idDict:
                    idDict[names[i][0]+" "+names[i][1]] = idNum
                    regionDict[idNum] = names[i][0]
                    for variant in variantDict[names[i][0]+" "+names[i][1]]:
                        idDict[variant] = idNum
                elif names[i][0]+" "+names[i][1] == "Amhara Oromia" and "Amhara Oromia" in idDict:
                    continue
                else:
                    idDict[names[i][1]] = idNum
                    regionDict[idNum] = names[i][0]
                    # If variants exist, add them
                    if names[i][1] in variantDict:
                        for variant in variantDict[names[i][1]]:
                            idDict[variant] = idNum
                idNum += 1
        nameFile.close()
    for k,v in idDict.items():
        print(f"""{v},Ethiopia CSA Livestock PDFs,Ethiopia,{k},{regionDict[v]}""", file=idFile)
    idFile.close()

    for y in range(startYear, endYear):
        year = str(y)

#--------------CREATE year_goats_category FROM year_Table_3-4 and year_Table_3-16--------------
        rfile1 = open(year+"_Table_3-4.csv", "r")
        rlist1 = list(csv.reader(rfile1, delimiter=','))
        rfile2 = None
        if year == "2003":
            rfile2 = open(year+"_Table_3-20.csv", "r")
        else:
            rfile2 = open(year + "_Table_3-16.csv", "r")
        rlist2 = list(csv.reader(rfile2, delimiter=','))
        #open file for writing
        wfile = open(year + "_goats_category.csv", "w")

        for i in range(1, len(rlist1)):
            id = str(getId(idDict, rlist1[i][:2]))
            print(id+","+year+","+rlist1[i][2]+","+rlist1[i][3]+","+rlist1[i][4]+","+rlist1[i][5]+","+rlist1[i][6]+","+rlist1[i][7]+","+rlist1[i][8]+","+rlist1[i][9]+","+rlist1[i][10]+","+rlist2[i][3]+","+rlist2[i][4]+","+rlist2[i][5]+","+rlist2[i][6]+","+rlist2[i][7]+","+rlist2[i][8] , file=wfile)

        rfile1.close()
        rfile2.close()
        wfile.close()

#--------------CREATE year_goats_usage FROM year_Table_3-9--------------
        rfile1 = open(year+"_Table_3-9.csv", "r")
        rlist1 = list(csv.reader(rfile1, delimiter=','))
        #open file for writing
        wfile = open(year + "_goats_usage.csv", "w")

        for i in range(1, len(rlist1)):
            id = str(getId(idDict, rlist1[i][:2]))
            print(id+","+year+","+rlist1[i][2]+","+rlist1[i][3]+","+rlist1[i][4]+","+rlist1[i][5]+","+rlist1[i][6]+","+rlist1[i][7]+","+rlist1[i][8]+","+rlist1[i][9], file=wfile)

        rfile1.close()
        wfile.close()

#--------------CREATE year_goats_estimation FROM year_Table_3-19c and year_Table_3-20c--------------
        if int(year) >= 2005:
            rfile1 = open(year+"_Table_3-19c.csv", "r")
            rlist1 = list(csv.reader(rfile1, delimiter=','))
            rfile2 = open(year + "_Table_3-20c.csv", "r")
            rlist2 = list(csv.reader(rfile2, delimiter=','))
            #open file for writing
            wfile = open(year + "_goats_estimation.csv", "w")

            for i in range(2, len(rlist1)):
                id = str(getId(idDict, rlist1[i][:2]))
                print(id+","+year+","+rlist1[i][2]+","+rlist1[i][3]+","+rlist1[i][4]+","+rlist1[i][5]+","+rlist1[i][6]+","+rlist1[i][7]+","+rlist1[i][8]+","+rlist1[i][9]+","+rlist1[i][10]+","+rlist2[i][2]+","+rlist2[i][3]+","+rlist2[i][4]+","+rlist2[i][5]+","+rlist2[i][6]+","+rlist2[i][7]+","+rlist2[i][11]+","+rlist2[i][12]+","+rlist2[i][13] , file=wfile)

            rfile1.close()
            rfile2.close()
            wfile.close()

#--------------CREATE year_goats_health--------------
        rfile3 = None
        rlist3 = None
        rfile4 = None
        rlist4 = None
        rfile5 = None
        rlist5 = None
        rfile6 = None
        rlist6 = None
        if year == "2003":
            rfile1 = open(year+"_Table_3-21.csv", "r")
            rfile2 = open(year + "_Table_3-22.csv", "r")
            rfile3 = open(year + "_Table_3-23.csv", "r")
            rfile4 = open(year + "_Table_3-24.csv", "r")
        elif year == "2004":
            rfile1 = open(year+"_Table_3-22.csv", "r")
            rfile2 = open(year + "_Table_3-23.csv", "r")
            rfile3 = open(year + "_Table_3-24.csv", "r")
            rfile4 = open(year + "_Table_3-25a.csv", "r")
            rfile5 = open(year + "_Table_3-25b.csv", "r")
            rlist5 = list(csv.reader(rfile5, delimiter=','))
        else:
            rfile1 = open(year+"_Table_3-23c.csv", "r")
            rfile2 = open(year + "_Table_3-20c.csv", "r")
            rfile3 = open(year + "_Table_3-24.csv", "r")
            rfile4 = open(year + "_Table_3-25.csv", "r")
            rfile5 = open(year + "_Table_3-26a.csv", "r")
            rlist5 = list(csv.reader(rfile5, delimiter=','))
            rfile6 = open(year + "_Table_3-26b.csv", "r")
            rlist6 = list(csv.reader(rfile6, delimiter=','))
        rlist1 = list(csv.reader(rfile1, delimiter=','))
        rlist2 = list(csv.reader(rfile2, delimiter=','))
        rlist3 = list(csv.reader(rfile3, delimiter=','))
        rlist4 = list(csv.reader(rfile4, delimiter=','))
        #open file for writing
        wfile = open(year + "_goats_health.csv", "w")
        #print differently based on year
        for i in range(1, len(rlist1)):
            id = str(getId(idDict, rlist1[i][:2]))
            if year == "2003":
                print(id+","+year+","+rlist2[i][4]+","+rlist3[i][4]+",0,0,"+rlist1[i][4]+",0,0,0,0,0,0,"+rlist4[i][4]+",0,0" , file=wfile)
            elif year == "2004":
                print(id+","+year+","+rlist2[i][4]+","+rlist3[i][4]+","+rlist4[i][4]+","+rlist5[i][4]+","+rlist1[i][4]+",0,0,0,0,0,0,0,0,0" , file=wfile)
            elif int(year) >= 2006 and int(year) <= 2009:
                print(id+","+year+","+rlist3[i][4]+","+rlist4[i][4]+","+rlist5[i][4]+","+rlist6[i][4]+","+rlist1[i][2]+","+rlist1[i][3]+","+rlist1[i][4]+","+rlist1[i][5]+","+rlist1[i][6]+","+rlist1[i][7]+","+rlist1[i][8]+","+rlist2[i+1][8]+","+rlist2[i+1][9]+","+rlist2[i+1][10] , file=wfile)
            elif year == "2020":
                print(id+","+year+","+rlist3[i][4]+","+rlist4[i][4]+","+rlist5[i][4]+","+rlist6[i][4]+","+rlist1[i][2]+","+rlist1[i][3]+","+rlist1[i][4]+","+rlist1[i][5]+","+rlist1[i][6]+",0,0,"+rlist2[i+1][8]+","+rlist2[i+1][9]+","+rlist2[i+1][10] , file=wfile)
            else:
                print(id+","+year+","+rlist3[i][4]+","+rlist4[i][4]+","+rlist5[i][4]+","+rlist6[i][4]+","+rlist1[i][2]+","+rlist1[i][3]+","+rlist1[i][4]+","+rlist1[i][5]+","+rlist1[i][6]+",0,"+rlist1[i][7]+","+rlist2[i+1][8]+","+rlist2[i+1][9]+","+rlist2[i+1][10] , file=wfile)

        rfile1.close()
        rfile2.close()
        rfile3.close()
        rfile4.close()
        if rfile5:
            rfile5.close()
        if rfile6:
            rfile6.close()
        wfile.close()

#--------------CREATE year_goats_holdings FROM year_Table_3-27c, 2004_Table_3-26c--------------
        if int(year) >= 2004:
            if year == "2004":
                rfile1 = open(year+"_Table_3-26c.csv", "r")
            else:
                rfile1 = open(year+"_Table_3-27c.csv", "r")
            rlist1 = list(csv.reader(rfile1, delimiter=','))
            #open file for writing
            wfile = open(year + "_goats_holdings.csv", "w")
            #print differently based on year
            for i in range(1, len(rlist1)):
                id = str(getId(idDict, rlist1[i][:2]))
                if int(year) >= 2019:
                    print(id+","+year+","+rlist1[i][2]+","+rlist1[i][3]+","+rlist1[i][4]+","+rlist1[i][5]+","+rlist1[i][6]+","+rlist1[i][7]+","+rlist1[i][8]+",0,0" , file=wfile)
                else:
                    # For years without total holding, calculate it and add it to the table
                    holdingList = [int(val) for val in rlist1[i][2:]]
                    totalHolding = str(sum(holdingList))
                    print(id+","+year+","+totalHolding+","+rlist1[i][2]+","+rlist1[i][3]+","+rlist1[i][4]+","+rlist1[i][5]+","+rlist1[i][6]+","+rlist1[i][7]+","+rlist1[i][8]+","+rlist1[i][9] , file=wfile)

            rfile1.close()
            wfile.close()
    

if __name__ == "__main__":
    main ( sys.argv[1:] )

#
# End of createGoatsDatabaseFiles.py
#