#!/usr/bin/env python
import requests 
from io import StringIO
import pandas as pd

api_url = 'https://dfe-redcap.azurewebsites.net/redcap/api/'
api_token = '80395861F2E51154EC9FD8E6FF037B0D'

# If selecting a subset of records; defaults to all records
records = list(range(0,1)) # generate a list of records to select
records = ','.join(str(i) for i in records) # parse list to a string

data = {
    'token': '80395861F2E51154EC9FD8E6FF037B0D',
    'content': 'record',
    'action': 'export',
    'format': 'csv',
    'type': 'flat',
    'csvDelimiter': '',
    'records': records, # Comment out to export all records
    'rawOrLabel': 'raw',
    'rawOrLabelHeaders': 'raw',
    'exportCheckboxLabel': 'false',
    'exportSurveyFields': 'false',
    'exportDataAccessGroups': 'false',
    'returnFormat': 'json'
}

r = requests.post(api_url, data=data)
df = pd.read_csv(StringIO(r.text), sep=',')

print('HTTP Status: ' + str(r.status_code))
print(r.text)
#print(df)
