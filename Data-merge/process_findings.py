#!/usr/bin/env python
import requests 
from io import StringIO
import pandas as pd
import numpy as np

# If selecting a subset of records; defaults to all records
#records = list(range(0,1)) # generate a list of records to select
#records = ','.join(str(i) for i in records) # parse list to a string

# Pull data from REDCap
data = {
    'token': '', # insert the API token
    'content': 'record',
    'action': 'export',
    'format': 'csv',
    'type': 'flat',
    #'csvDelimiter': '',
    #'records': records, # Comment out to export all records
    #'forms': 'icd10', # Comment out to export all forms
    'fields': 'case_number, cause_of_death, coronial_finding_made, coronial_finding', # Comment out to export all fields
    'filterLogic': '[exclude_case]=0 AND [coronial]=1',
    'rawOrLabel': 'raw',
    'rawOrLabelHeaders': 'raw',
    'exportCheckboxLabel': 'false',
    'exportSurveyFields': 'false',
    'exportDataAccessGroups': 'false',
    'returnFormat': 'json'
}

r = requests.post('https://dfe-redcap.azurewebsites.net/redcap/api/', data=data)
df = pd.read_csv(StringIO(r.text), sep=',', dtype=str)

print('HTTP Status: ' + str(r.status_code))
print(r.text)


# Process data
df.replace({np.nan: ''}, inplace=True)
df.set_index('case_number', inplace=True)

def process_findings(data):
    df = data.copy(deep=True)
    for i, row in df.iterrows():
        if "finding" in row['cause_of_death'].lower():
            row['coronial_finding'] = row["cause_of_death"]
            row["coronial_finding_made"] = '1'
        else:
            row["coronial_finding_made"] = '0'
    return df

df = process_findings(df)


# Import the data
# Write to the string 'records'
records = df.to_csv(sep="|")

# Data to post
data = {
    'token': '', # insert the API token
    'content': 'record',
    'action': 'import',
    'format': 'csv',
    'type': 'flat',
    'overwriteBehavior': 'normal',
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