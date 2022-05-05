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
with open("converted.txt", "r") as f:
    records = f.read()


# Data to post
data = {
    'token': '80395861F2E51154EC9FD8E6FF037B0D',
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
