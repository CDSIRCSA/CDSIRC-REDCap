#!/usr/bin/env python
import requests
import csv

# The data to import
file = 'C:/Users/jagvan/OneDrive - South Australia Government/REDCap/Data-merge/Data/test.csv'

# Change the delimiter from ',' to '|', allowing text fields with commas to be parsed
reader = csv.reader(open(file), delimiter = '|')
writer = csv.writer(open('converted.txt', 'w'), delimiter = '|')
writer.writerows(reader)

# Read the converted file and write to the string 'records'
records = ''
with open(file, "r", encoding = "utf8") as f:
    records = f.read()
records = records[1:]

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
    'returnFormat': 'csv',
    'csvDelimiter': '|'
}

# POST request 
r = requests.post('https://dfe-redcap.azurewebsites.net/redcap/api/', data=data)
print('HTTP Status: ' + str(r.status_code))
print(r.text)


data = {
    'token': '80395861F2E51154EC9FD8E6FF037B0D',
    'content': 'record',
    'action': 'import',
    'format': 'json',
    'type': 'flat',
    'overwriteBehavior': 'overwrite',
    'forceAutoNumber': 'false',
    'data': '[  {   "case_number": 136,   "screening_outcomes": "reviewable under 52S 2 a and bNot under 52S 3 c - there has been a history of contact, but outside the reporting period (1998)\\n\\n12-2006 Screened by medical team - not for ID review."  },  {   "case_number": 140,   "screening_outcomes": "Reviewable under 52S a a nd b\\n\\nProbably reviewable unde 52S 3 a and c\\n\\nScreened by Committee and determined to be for in-depth review. Request to review denied by coroner.\\n\\n01-2008 Coronial finding made in 2007 and case reviewed, awaiting final draft.\\n\\n10-04-08 Submitted to the Minister.\\n\\n10-09: Response to recommendations received from the Minister and reviewed by Fiona Ward and Nigel Stewart. They noted the same trend in these recommendations - statements concerning policies and draft policies with no indications regarding implementation and evaluation. Committee wants to write back to inquire about accountability, quality management and implementation - with an emphasis on asking about changes in practice."  } ]',
    'returnContent': 'count',
    'returnFormat': 'json'
}
r = requests.post('https://dfe-redcap.azurewebsites.net/redcap/api/',data=data)
print('HTTP Status: ' + str(r.status_code))
print(r.json())





