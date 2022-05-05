#!/usr/bin/env python
import requests

# If selecting a subset of records
# Put records in an array

#records = list(range(1,2000))

# Loop over records, deleting each one
for record in records:
    data = {
        'token': '80395861F2E51154EC9FD8E6FF037B0D',
        'action': 'delete',
        'content': 'record',
        'records[0]': str(record),
        'returnFormat': 'json'
    }
    
    # Only uncomment the following line if you really mean it!!!
    # r = requests.post('https://dfe-redcap.azurewebsites.net/redcap/api/',data=data)

    print('HTTP Status: ' + str(r.status_code))
    print(r.text)
    
    



