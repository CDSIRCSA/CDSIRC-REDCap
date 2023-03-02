#!/usr/bin/env python
import requests
import pyodbc
import pandas as pd
import os

# Connect to database and load data from scripts
# get the scripts
scripts = os.listdir("C:\\Users\\jagvan\OneDrive - South Australia Government\\Code\\SQL Server Management Studio\\Queries\\REDCap\\Pre-2005")

# do the first one so the rest can be joined
sql_query = open("C:\\Users\\jagvan\OneDrive - South Australia Government\\Code\\SQL Server Management Studio\\Queries\\REDCap\\Pre-2005\\"+scripts[0]).read()
conn = pyodbc.connect('DSN=CDR-DSN')
df = pd.read_sql_query(sql_query, conn, dtype = str, index_col = "case_number")

# loop over the remaining scripts and merge them into the dataframe
for script in scripts[1:]:
    sql_query = open("C:\\Users\\jagvan\\OneDrive - South Australia Government\\Code\\SQL Server Management Studio\\Queries\\REDCap\\Pre-2005\\"+script).read()
    conn = pyodbc.connect('DSN=CDR-DSN')
    df = df.merge(pd.read_sql_query(sql_query, conn, dtype = str, index_col = "case_number"), how="left", on="case_number")

# fix data
df['postcode'] = df['postcode'].replace({'    ': ''})
df = df.fillna('')
df = df.replace({'None': ''})

# Write to the string 'records'
records = df.to_csv(sep="|")


# Data to post
data = {
    'token': '', # insert the API token
    'content': 'record',
    'action': 'import',
    'format': 'csv',
    'type': 'flat',
    'overwriteBehavior': 'overwrite',
    'forceAutoNumber': 'false',
    'data': records,
    'dateFormat': 'DMY',
    'returnContent': 'count',
    'returnFormat': 'csv',
    'csvDelimiter': '|'
}

# POST request 
r = requests.post('https://dfe-redcap.azurewebsites.net/redcap/api/', data=data)
print('HTTP Status: ' + str(r.status_code))
print(r.text)

