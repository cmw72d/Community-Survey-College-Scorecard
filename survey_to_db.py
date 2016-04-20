import csv
import json
import glob
import os
import sqlite3

# Path to CSV files (may not contain any other files)
# Delete either the housing or people CSVs. The columns
# below are all from the Housing dataset
path = 'survey'

# Database
conn = sqlite3.connect('database.sqlite')

# Drop table so we don't create duplicates since we're about to reimport
conn.execute('''
    DROP TABLE IF EXISTS SURVEY
    ''')

# Create table
# STATE
# FAMILY TYPE
# FAMILY INCOME
conn.execute('''
    CREATE TABLE
    IF NOT EXISTS SURVEY(
        ST CHARACTER(2),
        FES INT,
        FINCP INT
    );''')

# Insert all data into database
for directory in os.listdir(path): # for each file in data directory
    for file in os.listdir(path): # for each file in each directory
        with open(path + '/' + file, encoding='ISO-8859-1') as a_file: # open csv file
            reader = csv.reader((line.replace('\0','') for line in a_file), delimiter=",", skipinitialspace=True, quoting=csv.QUOTE_NONE)
            for row in reader: # for each column enter into database
                conn.execute('INSERT INTO SURVEY VALUES (?,?,?);',(row[5],row[57],row[61]))
                
conn.commit()

conn.close()