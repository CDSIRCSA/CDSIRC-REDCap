# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 12:59:03 2021

@author: jagvan_adm
"""
import pandas as pd
import json

# Load ARIA data
ra_2006 = pd.read_csv("ra_2006.csv", dtype=str)
ra_2006.name = 2006
ra_2011 = pd.read_csv("ra_2011.csv", dtype=str)
ra_2011.name = 2011
ra_2016 = pd.read_csv("ra_2016.csv", dtype=str)
ra_2016.name = 2016

# JSONify the data
aria_dict = {}
for df in [ra_2006, ra_2011, ra_2016]:
    aria_dict[df.name] = {}
    for index, row in df.iterrows():
        aria_dict[df.name][row['postcode']] = row['ra_name']

# Write to file
with open("aria_dict.txt", 'w') as file:
    file.write(json.dumps(aria_dict))