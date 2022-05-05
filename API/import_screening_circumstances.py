#!/usr/bin/env python
import requests
import codecs

# The data to import
# File should be a pipe-separated values file. Use SSMS 'Results to File' with | as the delimiter
file = 'C:/Users/jagvan/OneDrive - South Australia Government/REDCap/Data-merge/Data/cod_circumstances050522.csv'
# Make sure any trailing text is removed (e.g. SSMS results statement)

# Read the file and write to the string 'records'
records = ''
with open(file, "r", encoding = "utf8") as f:
    records = f.read()
# Remove leading csv character
records = records[1:]
# Remove escape characters to make valid newlines ('\r')
records = codecs.decode(records, 'unicode-escape')

# Data to post
data = {
    'token': '80395861F2E51154EC9FD8E6FF037B0D',
    'content': 'record',
    'action': 'import',
    'format': 'csv',
    'type': 'flat',
    'overwriteBehavior': 'overwrite',
    'forceAutoNumber': 'false',
    'data': records,
    'dateFormat': 'DMY',
    'returnContent': 'count',
    'returnFormat': 'json',
    'csvDelimiter': '|'
}

# POST request 
r = requests.post('https://dfe-redcap.azurewebsites.net/redcap/api/', data=data)
print('HTTP Status: ' + str(r.status_code))
print(r.text)