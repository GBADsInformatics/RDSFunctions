# RDS_Functions

This repo contains Python3 scripts to manipulate the database publicData_1 on AWS RDS.

Because of security (password for database user), the function(s) that connect to the 
database are not included here.  Please contact Deb Stacey for that code.

## Installation

`pip3 install -r requirements.txt`

## Usage

### Querying Ethiopia CSA Livestock PDFs Data
`queryEthiopiaTables.py -t <table name> -c <country> -r <region> -z <zone> -y <year> -d <data field name> -s <datasource>`
* t = table name (table_name)
* c = country (qcountry)
* r = region (qregion)
* z = zone (qzone)
* y = year (qyear)
* d = data field name (dfield_name)
* s = datasource (qdatasource)
* **Note**: for examples, look in the script documentation

### Querying Ghana Aquaculture Data
`queryGhanaTables.py -t <table name> -r <region> -z <zone> -n <owner> -f <farm> -y <year> -c <culture system> -l <tech level> -w <water type> -o <water source> -s <species> -a <issueCode> -b <issueNum> -d <data field name> -i <id_auto>`
* t = table name (table_name)
* r = region (qregion)
* z = zone/district (qzone)
* n = owner name (qowner)
* f = farm name (qfarm)
* y = prod. year (qyear)
* c = culture system (qculture_system)
* l = technology level (qtech_level)
* w = water type (qwater_type)
* o = source of water (qwater_source)
* s = main species cultured (qspecies_cultured)
* d = data field name (dfield_name)
* i = id_auto (qID)

### Querying FAOSTAT Data
`queryFAOSTAT.py -t <table name> -c <country> -s <species> -y <year> -d <data field name>`
* t = table name (table_name)
* c = country (qcountry)
* s = species (qspecies)
* y = year (qyear)
* d = data field name (dfield_name)
* **Note**: for examples, look in the script documentation

### RDS Functions
* **Note**: for more documentation, refer to comments in files
* `createPublicTable.py` is used for creating database tables from schema files
* `dropPublicTable.py` is used for dropping database tables
* `loadTable.py` is used for loading in csv files into tables

## Other
* **Note**: for more documentation, refer to comments in files
* `createDBFiles` directory contains all the scripts used for creating database table files from a private repo for Ethiopia CSA Livestock PDFs
    * Each bash script must be ran with its python counterpart, `nameVariants.py` and has to have access to all year folders from mentioned private repo
    * **IMPORTANT**: All scripts in `createDBFiles` directory are only needed if data from the database is lost and needs to be recovered
* `schemas` directory contains all schemas used for the database
