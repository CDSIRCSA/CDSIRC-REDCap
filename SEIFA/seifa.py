# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 16:11:54 2021

@author: jagvan_adm
"""

import pandas as pd
import json

# Import SEIFA data
seifa2006 = pd.read_csv("seifa_2006.csv", dtype=str).dropna()
seifa2006.name = "2006"
seifa2011 = pd.read_csv("seifa_2011.csv", dtype=str).dropna()
seifa2011.name = "2011"
seifa2016 = pd.read_csv("seifa_2016.csv", dtype=str).dropna()
seifa2016.name = "2016"

# Fix 3-digit (08xx) postcodes
for df in [seifa2006, seifa2011, seifa2016]:
    for index, row in df.iterrows():
        if len(row['postcode']) == 3:
            row['postcode'] = "0" + row['postcode']
        
        
# JSONify
dict_2016 = {}
for index, row in seifa2016.iterrows():
    if not pd.isna(row[1]):
        dict_2016[row['postcode']] = int(row[1])
        
nested_dict = {}
for df in [seifa2006, seifa2011, seifa2016]:
    dfname = int(df.name)
    nested_dict[dfname] = {}
    for index, row in df.iterrows():
        nested_dict[dfname][row['postcode']] = {}
    for index, row in df.iterrows():        
        nested_dict[dfname][row['postcode']]['SEIFA_advantage_disadvantage'] = int(row['SEIFA_advantage_disadvantage'])
        nested_dict[dfname][row['postcode']]['SEIFA_disadvantage'] = int(row['SEIFA_disadvantage'])
        nested_dict[dfname][row['postcode']]['SEIFA_education_occupation'] = int(row['SEIFA_education_occupation'])
        nested_dict[dfname][row['postcode']]['SEIFA_economic'] = int(row['SEIFA_economic'])

# View and write the dict to a text file
print(nested_dict)
with open("nested_dict.txt", 'w') as file:
    file.write(json.dumps(nested_dict))
    
    