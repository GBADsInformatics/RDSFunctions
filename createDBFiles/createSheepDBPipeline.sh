#! /bin/sh
#
# Pipeline for extracting tar files from their respective folders, creating database files for each year and cleaning the extracted contents
#
echo "Extracting tar files for 2003-2020"
value=2003
while [ "$value" -le 2020 ]; do
    echo "Extracting ${value}_Sheep_Tables.tar..."
    tar -xf "${value}/${value}_Sheep_Tables.tar"
    value=$(( value + 1 ))
done
echo "Running createDatabaseFiles.py"
python3 createSheepDatabaseFiles.py
echo "Cleaning files..."
value=2003
while [ "$value" -le 2020 ]; do
    rm "${value}_T"*".csv"
    value=$(( value + 1 ))
done
