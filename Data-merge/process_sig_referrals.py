# -*- coding: utf-8 -*-
import requests 
from io import StringIO
import pandas as pd

# If selecting a subset of records; defaults to all records
#records = list(range(0,1)) # generate a list of records to select
#records = ','.join(str(i) for i in records) # parse list to a string

data = {
    'token': '', # insert the API token
    'content': 'record',
    'action': 'export',
    'format': 'csv',
    'type': 'flat',
    #'csvDelimiter': '',
    'fields': 'case_number, sig_referral', # Comment out to export all fields
    'filterLogic': '[exclude_case]=0',
    'rawOrLabel': 'raw',
    'rawOrLabelHeaders': 'raw',
    'exportCheckboxLabel': 'false',
    'exportSurveyFields': 'false',
    'exportDataAccessGroups': 'false',
    'returnFormat': 'json'
}

r = requests.post('https://dfe-redcap.azurewebsites.net/redcap/api/', data=data)
df = pd.read_csv(StringIO(r.text), sep=',')

print('HTTP Status: ' + str(r.status_code))


#----------------------------------
# Rename columns to convert to the new variables
df.rename(columns={'health_sig___1':'health_sig',
           'cp_sig___1':'cp_sig',
           'aboriginal_sig___1':'aboriginal_sig',
           'cald_sig___1':'cald_sig',
           'child_safety_sig___1':'child_safety_sig',
           'suicide_prevention_sig___1':'suicide_prevention_sig',
           'disability_sig___1':'disability_sig'}, inplace=True)

df.set_index('case_number',inplace=True)
df.drop(columns=['sig_referral___0'], inplace=True)
df.replace({0:''}, inplace=True)

#----------------------------------
# Import data
records = df.to_csv(sep="|")

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