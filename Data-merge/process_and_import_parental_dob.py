# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import requests
from io import StringIO

# Export and load the data
data = {
    'token': '', # insert the API token
    'content': 'record',
    'action': 'export',
    'format': 'csv',
    'type': 'flat',
    #'csvDelimiter': '',
    #'records': records, # Comment out to export all records
    #'forms': 'icd10', # Comment out to export all forms
    'fields': 'case_number, mother_dob, father_dob', # Comment out to export all fields
    #'filterLogic': '[exclude_case]=0',
    'rawOrLabel': 'label',
    'rawOrLabelHeaders': 'raw',
    'exportCheckboxLabel': 'false',
    'exportSurveyFields': 'false',
    'exportDataAccessGroups': 'false',
    'returnFormat': 'json'
}

r = requests.post('https://dfe-redcap.azurewebsites.net/redcap/api/', data=data)
redcap_data = pd.read_csv(StringIO(r.text), sep=',')

df = pd.read_csv('C:/Users/jagvan/OneDrive - South Australia Government/REDCap/Data-merge/Data/parental_dob_bdm_linkage.csv')


# Join the data
joined = pd.merge(redcap_data, df, how="outer", on="case_number")

# Replace nulls
joined.replace({np.nan: ''}, inplace=True)

# Process the data
joined['mother_dob'] = joined.apply(lambda x: x.mother_dob_x if x.mother_dob_x != '' else x.mother_dob_y, axis=1)
joined['father_dob'] = joined.apply(lambda x: x.father_dob_x if x.father_dob_x != '' else x.father_dob_y, axis=1)
joined = joined.loc[:,['case_number','mother_dob','father_dob']]

joined.set_index('case_number', inplace=True)

# Write to the string 'records'
records = joined.to_csv(sep="|")


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





