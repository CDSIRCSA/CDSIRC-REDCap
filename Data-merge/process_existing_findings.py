#!/usr/bin/env python
import os
import requests 
from io import StringIO
import pandas as pd
import numpy as np
from datetime import date

# ----------------------------------
# Load in findings spreadsheets
directory = "Findings"
findings = pd.DataFrame()
findings = pd.read_csv("Findings\BDMSA cdr cause of death data 202210.csv", engine='python', dtype=str, skipfooter=1)

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        findings = pd.concat([findings,pd.read_csv(f, engine='python', dtype=str, skipfooter=1)])

findings.set_index('Registration Number', inplace=True)
findings.replace({np.nan: ''}, inplace=True)

# ----------------------------------
# Pull data from REDCap
# Filter for cases where a coronial finding has not been recorded
data = {
    'token': '', # insert the API token
    'content': 'record',
    'action': 'export',
    'format': 'csv',
    'type': 'flat',
    #'csvDelimiter': '',
    #'records': records, # Comment out to export all records
    #'forms': 'icd10', # Comment out to export all forms
    'fields': 'case_number, bdm_id, coronial_finding_made, coronial_finding', # Comment out to export all fields
    'filterLogic': '[exclude_case]=0 AND [coronial]=1 AND [coronial_finding_made]=0 AND [bdm_id]!=""',
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


# ----------------------------------
# Process data
df.replace({np.nan: ''}, inplace=True)
df.set_index('case_number', inplace=True)

cod_fields = ["Cause of Death 1B", "Cause of Death 1C", "Cause of Death 1D", "Cause of Death 1E", "Cause of Death 2A", "Cause of Death 2B", "Cause of Death 2C", "Cause of Death 2D", "Cause of Death 2E"]
def process_findings(data):
    df = data.copy(deep=True)
    for i, row in df.iterrows():
        if row['bdm_id'] in findings.index:
            row['coronial_finding_made'] = '1'
            row['coronial_finding'] = "FINDING (" + date.today().strftime('%d/%m/%Y') + "): " + findings.loc[row['bdm_id'], 'Cause of Death 1A']
            for field in cod_fields:
                if findings.loc[row['bdm_id'], field] != '':
                    row['coronial_finding'] = row['coronial_finding'] + "; " + findings.loc[row['bdm_id'], field]
    return df

df = process_findings(df)


# ----------------------------------
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