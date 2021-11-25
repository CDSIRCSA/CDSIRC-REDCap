# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 16:11:54 2021

@author: jagvan_adm
"""

import pandas as pd

seifa2006 = pd.read_csv("seifa_2006.csv", dtype=str)
seifa2006 = seifa2006.iloc[:,[0,2]]
seifa2011 = pd.read_csv("seifa_2011.csv", dtype=str)
seifa2011 = seifa2011.iloc[:,[0,2]]
seifa2016 = pd.read_csv("seifa_2016.csv", dtype=str)
seifa2016 = seifa2016.iloc[:,[0,2]]

dflist = [seifa2006, seifa2011, seifa2016]
for df in dflist:
    print(df['postcode'].head())

for index, row in seifa2016.iterrows():
    if len(row['postcode']) == 3:
        row['postcode'] = "0" + row['postcode']

string = ""
for row in seifa2006.itertuples(index=False):
    if row.SEIFA_disadvantage == 5.0:
        string = string + " or [postcode]=" + str(row.postcode)
        
        
# JSON
dict_2016 = {}
for index, row in seifa2016.iterrows():
    if not pd.isna(row[1]):
        dict_2016[row['postcode']] = int(row[1])
        
    
print(dict_2016)
