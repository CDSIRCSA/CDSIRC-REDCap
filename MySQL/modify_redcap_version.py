# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 11:16:29 2021

@author: jagvan_adm
"""

import mysql.connector

mydb = mysql.connector.connect(
    host = "edu-redcap-mysql01.mysql.database.azure.com",
    user = "AdminREDCap@edu-redcap-mysql01",
    password = "bubbaluboyA13`", 
    ssl_disabled = True
    )

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")
for x in mycursor:
    print(x)
    
mydb = mysql.connector.connect(
    host = "edu-redcap-mysql01.mysql.database.azure.com",
    user = "AdminREDCap@edu-redcap-mysql01",
    password = "bubbaluboyA13`", 
    ssl_disabled = True,
    database = "redcap"
    )
mycursor = mydb.cursor()
mycursor.execute("select field_name, value from redcap_config where field_name = 'redcap_version'")
mycursor.fetchall()
for x in mycursor.fetchall():
    print(x)
    
query = "UPDATE redcap_config SET value = '11.4.0' WHERE field_name = 'redcap_version'"
mycursor.execute(query)  
mydb.commit()    
    
    