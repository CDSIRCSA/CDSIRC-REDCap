# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 14:21:21 2021

@author: jagvan_adm
"""

import pandas as pd

regions = pd.read_excel("gov_regions_retouched.xlsx", dtype=str).drop_duplicates()

regions_dict = {}

for index, row in regions.iterrows():
    regions_dict[row['Postcode']] = row['SA Government Region']

print(json.dumps(regions_dict))
