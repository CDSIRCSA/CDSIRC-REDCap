# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import requests

df = pd.read_csv('Data/CALD updated cases 2022 June 15 for Jago.csv', dtype=str)

df.replace({np.nan: ''}, inplace=True)

df.rename(columns={'Casenumber':'case_number',
           'CALDstatus':'cald',
           'FamilyCALD':'parents_cald_background',
           'CALDStatusSourceBDM':'cald_sources___1',
           'CALDStatusSourcePOU':'cald_sources___2',
           'CALDStatusSourceCDR':'cald_sources___3',
           'Country_fath':'father_country_of_birth',
           'Country_moth':'mother_country_of_birth',
           'Country_child':'country_of_birth'},
          inplace=True)

df['cald'] = df['cald'].replace({'3':'0'}) # recode the 'Unknown' value
df['parents_cald_background'] = df['parents_cald_background'].replace({'9':'0'}) # recode the 'Unknown' value
df.drop(['Countrygrp','Countrygrp2'], axis=1, inplace=True)

# Process countries of birth
    # Clean up countries
df.replace({'Aus':'Australia',
            'Au':'Australia',
            'NZ':'New Zealand',
            'Bosnia and Herzegovi':'Bosnia and Herzegovina',
            'The Netherlands':'Netherlands',
            'Holland':'Netherlands',
            'Azad Kashmir':'Pakistan', #not recognised by ABS
            'Western Samoa':'Samoa',
            'Burma':'Myanmar',
            'Phillipines':'Philippines', 'Philipines':'Philippines',
            'USA':'United States of America',
            'Yugoslavia':'Serbia', # could be Montenegro
            'Mauretius':'Mauritius',
            'Africa':'Southern and East Africa, nec', # in the absence of a specific country
            'Russia':'Russian Federation',
            'Fiji Islands':'Fiji',
            'Papua New Guinea - n':'Papua New Guinea',
            'Papa New Guinea':'Papua New Guinea',
            'Sierre Leone':'Sierra Leone',
            'Congo':'Congo, Democratic Republic of',
            'Unk':'', # Unknown
            'Korea':'South Korea', # Assume South
            'Czech Republic':'Czechia',
            'Bangledesh':'Bangladesh',
            'Indian':'India'}, inplace=True) 

    # Dict of countries and codes
countries_dict = {'Australia': 1101, 'Norfolk Island': 1102, 'Australian External Territories, nec': 1199, 'New Zealand': 1201, 'New Caledonia': 1301, 'Papua New Guinea': 1302, 'Solomon Islands': 1303, 'Vanuatu': 1304, 'Guam': 1401, 'Kiribati': 1402, 'Marshall Islands': 1403, 'Micronesia, Federated States of': 1404, 'Nauru': 1405, 'Northern Mariana Islands': 1406, 'Palau': 1407, 'Cook Islands': 1501, 'Fiji': 1502, 'French Polynesia': 1503, 'Niue': 1504, 'Samoa': 1505, 'Samoa, American': 1506, 'Tokelau': 1507, 'Tonga': 1508, 'Tuvalu': 1511, 'Wallis and Futuna': 1512, 'Pitcairn Islands': 1513, 'Polynesia (excludes Hawaii), nec': 1599, 'Adelie Land (France)': 1601, 'Argentinian Antarctic Territory': 1602, 'Australian Antarctic Territory': 1603, 'British Antarctic Territory': 1604, 'Chilean Antarctic Territory': 1605, 'Queen Maud Land (Norway)': 1606, 'Ross Dependency (New Zealand)': 1607, 'England': 2102, 'Isle of Man': 2103, 'Northern Ireland': 2104, 'Scotland': 2105, 'Wales': 2106, 'Guernsey': 2107, 'Jersey': 2108, 'Ireland': 2201, 'Austria': 2301, 'Belgium': 2302, 'France': 2303, 'Germany': 2304, 'Liechtenstein': 2305, 'Luxembourg': 2306, 'Monaco': 2307, 'Netherlands': 2308, 'Switzerland': 2311, 'Denmark': 2401, 'Faroe Islands': 2402, 'Finland': 2403, 'Greenland': 2404, 'Iceland': 2405, 'Norway': 2406, 'Sweden': 2407, 'Aland Islands': 2408, 'Andorra': 3101, 'Gibraltar': 3102, 'Holy See': 3103, 'Italy': 3104, 'Malta': 3105, 'Portugal': 3106, 'San Marino': 3107, 'Spain': 3108, 'Albania': 3201, 'Bosnia and Herzegovina': 3202, 'Bulgaria': 3203, 'Croatia': 3204, 'Cyprus': 3205, 'North Macedonia': 3206, 'Greece': 3207, 'Moldova': 3208, 'Romania': 3211, 'Slovenia': 3212, 'Montenegro': 3214, 'Serbia': 3215, 'Kosovo': 3216, 'Belarus': 3301, 'Czechia': 3302, 'Estonia': 3303, 'Hungary': 3304, 'Latvia': 3305, 'Lithuania': 3306, 'Poland': 3307, 'Russian Federation': 3308, 'Slovakia': 3311, 'Ukraine': 3312, 'Algeria': 4101, 'Egypt': 4102, 'Libya': 4103, 'Morocco': 4104, 'Sudan': 4105, 'Tunisia': 4106, 'Western Sahara': 4107, 'Spanish North Africa': 4108, 'South Sudan': 4111, 'Bahrain': 4201, 'Gaza Strip and West Bank': 4202, 'Iran': 4203, 'Iraq': 4204, 'Israel': 4205, 'Jordan': 4206, 'Kuwait': 4207, 'Lebanon': 4208, 'Oman': 4211, 'Qatar': 4212, 'Saudi Arabia': 4213, 'Syria': 4214, 'Turkey': 4215, 'United Arab Emirates': 4216, 'Yemen': 4217, 'Myanmar': 5101, 'Cambodia': 5102, 'Laos': 5103, 'Thailand': 5104, 'Vietnam': 5105, 'Brunei Darussalam': 5201, 'Indonesia': 5202, 'Malaysia': 5203, 'Philippines': 5204, 'Singapore': 5205, 'Timor-Leste': 5206, 'China': 6101, 'Hong Kong': 6102, 'Macau': 6103, 'Mongolia': 6104, 'Taiwan': 6105, 'Japan': 6201, 'North Korea': 6202, 'South Korea': 6203, 'Bangladesh': 7101, 'Bhutan': 7102, 'India': 7103, 'Maldives': 7104, 'Nepal': 7105, 'Pakistan': 7106, 'Sri Lanka': 7107, 'Afghanistan': 7201, 'Armenia': 7202, 'Azerbaijan': 7203, 'Georgia': 7204, 'Kazakhstan': 7205, 'Kyrgyzstan': 7206, 'Tajikistan': 7207, 'Turkmenistan': 7208, 'Uzbekistan': 7211, 'Bermuda': 8101, 'Canada': 8102, 'St Pierre and Miquelon': 8103, 'United States of America': 8104, 'Argentina': 8201, 'Bolivia': 8202, 'Brazil': 8203, 'Chile': 8204, 'Colombia': 8205, 'Ecuador': 8206, 'Falkland Islands': 8207, 'French Guiana': 8208, 'Guyana': 8211, 'Paraguay': 8212, 'Peru': 8213, 'Suriname': 8214, 'Uruguay': 8215, 'Venezuela': 8216, 'South America, nec': 8299, 'Belize': 8301, 'Costa Rica': 8302, 'El Salvador': 8303, 'Guatemala': 8304, 'Honduras': 8305, 'Mexico': 8306, 'Nicaragua': 8307, 'Panama': 8308, 'Anguilla': 8401, 'Antigua and Barbuda': 8402, 'Aruba': 8403, 'Bahamas': 8404, 'Barbados': 8405, 'Cayman Islands': 8406, 'Cuba': 8407, 'Dominica': 8408, 'Dominican Republic': 8411, 'Grenada': 8412, 'Guadeloupe': 8413, 'Haiti': 8414, 'Jamaica': 8415, 'Martinique': 8416, 'Montserrat': 8417, 'Puerto Rico': 8421, 'St Kitts and Nevis': 8422, 'St Lucia': 8423, 'St Vincent and the Grenadines': 8424, 'Trinidad and Tobago': 8425, 'Turks and Caicos Islands': 8426, 'Virgin Islands, British ': 8427, 'Virgin Islands': 8428, 'St Barthelemy': 8431, 'St Martin': 8432, 'Bonaire, Sint Eustatius and Saba': 8433, 'Curacao': 8434, 'Sint Maarten': 8435, 'Benin': 9101, 'Burkina Faso': 9102, 'Cameroon': 9103, 'Cabo Verde': 9104, 'Central African Republic': 9105, 'Chad': 9106, 'Congo, Republic of': 9107, 'Congo, Democratic Republic of': 9108, "Cote d'Ivoire": 9111, 'Equatorial Guinea': 9112, 'Gabon': 9113, 'Gambia': 9114, 'Ghana': 9115, 'Guinea': 9116, 'Guinea-Bissau': 9117, 'Liberia': 9118, 'Mali': 9121, 'Mauritania': 9122, 'Niger': 9123, 'Nigeria': 9124, 'Sao Tome and Principe': 9125, 'Senegal': 9126, 'Sierra Leone': 9127, 'Togo': 9128, 'Angola': 9201, 'Botswana': 9202, 'Burundi': 9203, 'Comoros': 9204, 'Djibouti': 9205, 'Eritrea': 9206, 'Ethiopia': 9207, 'Kenya': 9208, 'Lesotho': 9211, 'Madagascar': 9212, 'Malawi': 9213, 'Mauritius': 9214, 'Mayotte': 9215, 'Mozambique': 9216, 'Namibia': 9217, 'Reunion': 9218, 'Rwanda': 9221, 'St Helena': 9222, 'Seychelles': 9223, 'Somalia': 9224, 'South Africa': 9225, 'Eswatini': 9226, 'Tanzania': 9227, 'Uganda': 9228, 'Zambia': 9231, 'Zimbabwe': 9232, 'Southern and East Africa, nec': 9299}
    
    # Assign the codes
def country_of_birth(data):
    df = data.copy(deep=True)
    cob_fields = ['country_of_birth','father_country_of_birth','mother_country_of_birth']
    for i, row in df.iterrows():
        for field in cob_fields:
            if row[field] != "":
                if row[field] in countries_dict.keys():
                    df.at[i, field] = str(countries_dict[row[field]])
                else:
                    print("Error: case {}, field '{}', country '{}'".format(row['case_number'], field, row[field]))
    return df

df = country_of_birth(df)

# Process country groups
country_groups = {
            '1': {'name': 'Oceania and Antarctica',
                'codes': {'11': 'Australia (includes External Territories)', '12': 'New Zealand', '13': 'Melanesia', '14': 'Micronesia', '15': 'Polynesia (excludes Hawaii)', '16': 'Antarctica'}},
            '2': {'name': 'North-West Europe',
                'codes': {'21': 'United Kingdom, Channel Islands and Isle of Man', '22': 'Ireland', '23': 'Western Europe', '24': 'Northern Europe'}},
            '3': {'name': 'Southern and Eastern Europe',
                'codes': {'31': 'Southern Europe', '32': 'South Eastern Europe', '33': 'Eastern Europe'}},
            '4': {'name': 'North Africa and the Middle East',
                'codes': {'41': 'North Africa', '42': 'Middle East'}},
            '5': {'name': 'South-East Asia',
                'codes': {'51': 'Mainland South-East Asia', '52': 'Maritime South-East Asia'}},
            '6': {'name': 'North-East Asia',
                'codes': {'61': 'Chinese Asia (includes Mongolia)', '62': 'Japan and the Koreas'}},
            '7': {'name': 'Southern and Central Asia',
                'codes': {'71': 'Southern Asia', '72': 'Central Asia'}},
            '8': {'name': 'Americas',
                'codes': {'81': 'Northern America', '82': 'South America', '83': 'Central America', '84': 'Caribbean'}},
            '9': {'name': 'Sub-Saharan Africa',
                'codes': {'91': 'Central and West Africa', '92': 'Southern and East Africa'}}}

def major_group(row, field):
    if row[field]:
        major_code = row[field][0]
        major_group = country_groups[major_code]['name']
        return major_group
    else: 
        return '' 

def minor_group(row, field):
    if row[field]:
        major_code = row[field][0]
        minor_code = row[field][0:2]
        minor_group = country_groups[major_code]['codes'][minor_code]
        return minor_group
    else:
        return ''

df['child_major_group'] = df.apply(lambda row: major_group(row, 'country_of_birth'), axis=1)
df['child_minor_group'] = df.apply(lambda row: minor_group(row, 'country_of_birth'), axis=1)
df['mother_major_group'] = df.apply(lambda row: major_group(row, 'mother_country_of_birth'), axis=1)
df['mother_minor_group'] = df.apply(lambda row: minor_group(row, 'mother_country_of_birth'), axis=1)
df['father_major_group'] = df.apply(lambda row: major_group(row, 'father_country_of_birth'), axis=1)
df['father_minor_group'] = df.apply(lambda row: minor_group(row, 'father_country_of_birth'), axis=1) 

######################################
# Load the data into REDCap
df.set_index('case_number', inplace=True)

    # Write to the string 'records'
records = df.to_csv(sep="|")


    # Data to post
data = {
    'token': '', # insert the API token
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





