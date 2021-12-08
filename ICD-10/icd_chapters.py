# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 16:54:33 2021

@author: jagvan_adm
"""

import pandas as pd
import json

chapters = pd.read_csv("icd-10-chapters.csv")

chapter_dict = {}
for index, row in chapters.iterrows():
    chapter_dict[row.Chapter] = {"Name": row.Name,
                                 "Codes": row.Codes}
    
with open("chapter_dict.txt", 'w') as file:
    file.write(json.dumps(chapter_dict))
        
place_codes = {0:"Home", 1:"Residential institution", 2:"School, other institution and public administrative area", 3:"Sports and athletics area", 4:"Street and highway", 5:"Trade and service area", 6:"Industrial and construction area", 7:"Farm", 8:"Other specified places", 9:"Unspecified place"}

activity_codes = {0:"While engaged in sports activity", 1:"While engaged in leisure activity", 2:"While working for income", 3:"While engaged in other types of work", 4:"While resting, sleeping, eating or engaging in other vital activities", 8:"While engaged in other specified activities", 9:"During unspecified activity"}

