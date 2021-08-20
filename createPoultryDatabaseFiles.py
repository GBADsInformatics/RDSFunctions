# 
# Author: Rehan Nagoor & Maxim Brochin
# 
# Last Update: August 19, 2021
# 
# Actions:
# - creates the appropriate poultry files to upload into the database 
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
        print ( "createCattleCategory.py" )
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ( "createCattleCategory.py" )
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
        print(f"""{v},Ethiopia,{regionDict[v]},{k},Ethiopia CSA Livestock PDFs""", file=idFile)
    idFile.close()

    for y in range(startYear, endYear):
        year = str(y)
#--------------CREATE year_poultry_inventory FROM year_Table_3-17a, year_Table_3-17b, year_Table_3-17c & year_Table_3-17d--------------
        rfile1 = None
        rlist1 = None
        rfile2 = None
        rlist2 = None
        rfile3 = None
        rlist3 = None
        rfile4 = None
        rlist4 = None
        if year == "2003":
            rfile1 = open(year+"_Table_3-14.csv", "r")
        elif year == "2004":
            rfile1 = open(year+"_Table_3-18a.csv", "r")
            rfile2 = open(year+"_Table_3-18b.csv", "r")
            rlist2 = list(csv.reader(rfile2, delimiter=','))
            rfile3 = open(year+"_Table_3-18c.csv", "r")
            rlist3 = list(csv.reader(rfile3, delimiter=','))
        else:
            rfile1 = open(year+"_Table_3-17a.csv", "r")
            rfile2 = open(year+"_Table_3-17b.csv", "r")
            rlist2 = list(csv.reader(rfile2, delimiter=','))
            rfile3 = open(year+"_Table_3-17c.csv", "r")
            rlist3 = list(csv.reader(rfile3, delimiter=','))
            rfile4 = open(year+"_Table_3-17d.csv", "r")
            rlist4 = list(csv.reader(rfile4, delimiter=','))
        rlist1 = list(csv.reader(rfile1, delimiter=','))
        #open file for writing
        wfile = open(year + "_poultry_inventory.csv", "w")

        for i in range(1, len(rlist1)):
            id = str(getId(idDict, rlist1[i][:2]))
            if year == "2003":
                print(id+","+year+","+rlist1[i][2]+","+rlist1[i][3]+","+rlist1[i][4]+","+rlist1[i][5]+","+rlist1[i][6]+","+rlist1[i][7]+","+rlist1[i][8]+",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0" , file=wfile)
            elif year == "2004":
                print(id+","+year+","+rlist1[i][2]+","+rlist1[i][3]+","+rlist1[i][4]+","+rlist1[i][5]+","+rlist1[i][6]+","+rlist1[i][7]+","+rlist1[i][8]+","+rlist2[i][2]+","+rlist2[i][3]+","+rlist2[i][4]+","+rlist2[i][5]+","+rlist2[i][6]+","+rlist2[i][7]+","+rlist2[i][8]+",0,0,0,0,0,0,0,"+rlist3[i][2]+","+rlist3[i][3]+","+rlist3[i][4]+","+rlist3[i][5]+","+rlist3[i][6]+","+rlist3[i][7]+","+rlist3[i][8] , file=wfile)
            else:
                print(id+","+year+","+rlist1[i][2]+","+rlist1[i][3]+","+rlist1[i][4]+","+rlist1[i][5]+","+rlist1[i][6]+","+rlist1[i][7]+","+rlist1[i][8]+","+rlist2[i][2]+","+rlist2[i][3]+","+rlist2[i][4]+","+rlist2[i][5]+","+rlist2[i][6]+","+rlist2[i][7]+","+rlist2[i][8]+","+rlist3[i][2]+","+rlist3[i][3]+","+rlist3[i][4]+","+rlist3[i][5]+","+rlist3[i][6]+","+rlist3[i][7]+","+rlist3[i][8]+","+rlist4[i][2]+","+rlist4[i][3]+","+rlist4[i][4]+","+rlist4[i][5]+","+rlist4[i][6]+","+rlist4[i][7]+","+rlist4[i][8] , file=wfile)

        rfile1.close()
        if rfile2:
            rfile2.close()
        if rfile3:
            rfile3.close()
        if rfile4:
            rfile4.close()
        wfile.close()

#--------------CREATE year_poultry_estimation FROM year_Table_3-19h and year_Table_3-20h--------------
        if int(year) >= 2005:
            rfile1 = open(year+"_Table_3-19h.csv", "r")
            rlist1 = list(csv.reader(rfile1, delimiter=','))
            rfile2 = open(year + "_Table_3-20h.csv", "r")
            rlist2 = list(csv.reader(rfile2, delimiter=','))
            #open file for writing
            wfile = open(year + "_poultry_estimation.csv", "w")

            for i in range(1, len(rlist1)):
                id = str(getId(idDict, rlist1[i][:2]))
                print(id+","+year+","+rlist1[i][2]+","+rlist1[i][3]+","+rlist1[i][4]+","+rlist2[i][2]+","+rlist2[i][3]+","+rlist2[i][4]+","+rlist2[i][5] , file=wfile)

            rfile1.close()
            rfile2.close()
            wfile.close()

#--------------CREATE year_poultry_eggs FROM year_Table_3-22a, year_Table_3-22b, year_Table3-22c & 2004_Table_3-21---------------
        if int(year) >= 2004:
            if year == "2004":
                rfile1 = open(year+"_Table_3-21.csv", "r")
            else:
                rfile1 = open(year+"_Table_3-22a.csv", "r")
                rfile2 = open(year+"_Table_3-22b.csv", "r")
                rlist2 = list(csv.reader(rfile2, delimiter=','))
                rfile3 = open(year+"_Table_3-22c.csv", "r")
                rlist3 = list(csv.reader(rfile3, delimiter=','))
            rlist1 = list(csv.reader(rfile1, delimiter=','))
            #open file for writing
            wfile = open(year + "_poultry_eggs.csv", "w")

            for i in range(1, len(rlist1)):
                if year == "2004" and i < len(rlist1)-1:
                    id = str(getId(idDict, rlist1[i+1][:2]))
                    print(id+","+year+","+rlist1[i+1][2]+","+rlist1[i+1][3]+","+rlist1[i+1][4]+","+rlist1[i+1][5]+","+rlist1[i+1][6]+",0,0,0,0,0,"+rlist1[i+1][7]+","+rlist1[i+1][8]+","+rlist1[i+1][9]+","+rlist1[i+1][10]+","+rlist1[i+1][11] , file=wfile)
                elif int(year) >= 2005:
                    id = str(getId(idDict, rlist1[i][:2]))
                    print(id+","+year+","+rlist1[i][2]+","+rlist1[i][3]+","+rlist1[i][4]+","+rlist1[i][5]+","+rlist1[i][6]+","+rlist2[i][2]+","+rlist2[i][3]+","+rlist2[i][4]+","+rlist2[i][5]+","+rlist2[i][6]+","+rlist3[i][2]+","+rlist3[i][3]+","+rlist3[i][4]+","+rlist3[i][5]+","+rlist3[i][6] , file=wfile)

            rfile1.close()
            rfile2.close()
            rfile3.close()

#--------------CREATE year_poultry_health--------------
        rfile5 = None
        rlist5 = None
        rfile6 = None
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
            rfile1 = open(year+"_Table_3-20h.csv", "r")
            rfile2 = open(year+"_Table_3-24.csv", "r")
            rfile3 = open(year + "_Table_3-25.csv", "r")
            rfile4 = open(year + "_Table_3-26a.csv", "r")
            rfile5 = open(year + "_Table_3-26b.csv", "r")
            rlist5 = list(csv.reader(rfile5, delimiter=','))
        rlist1 = list(csv.reader(rfile1, delimiter=','))
        rlist2 = list(csv.reader(rfile2, delimiter=','))
        rlist3 = list(csv.reader(rfile3, delimiter=','))
        rlist4 = list(csv.reader(rfile4, delimiter=','))
        #open file for writing
        wfile = open(year + "_poultry_health.csv", "w")
        #print differently based on year
        for i in range(1, len(rlist1)):
            id = str(getId(idDict, rlist1[i][:2]))
            if year == "2003":
                print(id+","+year+","+rlist2[i][7]+","+rlist3[i][7]+",0,0,"+rlist1[i][7]+","+rlist4[i][7] , file=wfile)
            elif year == "2004":
                print(id+","+year+","+rlist2[i][7]+","+rlist3[i][7]+","+rlist4[i][7]+","+rlist5[i][7]+","+rlist1[i][7]+",0" , file=wfile)
            else:
                print(id+","+year+","+rlist2[i][7]+","+rlist3[i][7]+","+rlist4[i][9]+","+rlist5[i][9]+",0,"+rlist1[i][4] , file=wfile)

        rfile1.close()
        rfile2.close()
        rfile3.close()
        rfile4.close()
        if rfile5:
            rfile5.close()
        wfile.close()

#--------------CREATE year_poultry_holdings FROM year_Table_3-27f, 2004_Table_3-26f--------------
        if int(year) >= 2004:
            if year == "2004":
                rfile1 = open(year+"_Table_3-26f.csv", "r")
            else:
                rfile1 = open(year+"_Table_3-27f.csv", "r")
            rlist1 = list(csv.reader(rfile1, delimiter=','))
            #open file for writing
            wfile = open(year + "_poultry_holdings.csv", "w")
            #print differently based on year
            for i in range(1, len(rlist1)):
                id = str(getId(idDict, rlist1[i][:2]))
                # calculate the total holdings and add it to the table
                holdingList = [int(val) for val in rlist1[i][2:]]
                totalHolding = str(sum(holdingList))
                print(id+","+year+","+totalHolding+","+rlist1[i][2]+","+rlist1[i][3]+","+rlist1[i][4]+","+rlist1[i][5]+","+rlist1[i][6]+","+rlist1[i][7] , file=wfile)

            rfile1.close()
            wfile.close()
    

if __name__ == "__main__":
    main ( sys.argv[1:] )

#
# End of createPoultryDatabaseFiles.py
#