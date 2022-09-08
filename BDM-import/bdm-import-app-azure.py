# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime
import json
import re

st.title('BDM list to REDCap converter')
#st.subheader('Upload a BDM list')
bdm_list = st.file_uploader(label='Upload a BDM list (.csv)',
                            type=['csv'])

if bdm_list:

    #df = pd.read_csv("bdm_list.csv", index_col=False, engine='python', skipfooter=1, dtype=str) # dev only
    df = pd.read_csv(bdm_list, index_col=False, engine='python', dtype=str)
    df = df[~df['Reg No'].str.startswith('T')] # Delete counter row
    df.index.rename('case_number', inplace=True)
    
    # Recode values and remove nans
    df = df.replace({'Sex':{'M': 1, 'F': 2},
                     'Coroner Indicator': {'M': 0, 'S': 1}})
    df = df.replace({np.nan: ''})
          
    df['exclude_case'] = '0' 
    
    # Convert names to title case
    df[['Surname','Given Names','Surname of Father','Surname of Father at Birth','Given Names of Father','Surname of Mother','Surname of Mother at Birth','Given Names of Mother','Doctors Name']] = df[['Surname','Given Names','Surname of Father','Surname of Father at Birth','Given Names of Father','Surname of Mother','Surname of Mother at Birth','Given Names of Mother','Doctors Name']].apply(lambda x: x.str.title(), axis=1)
    
    # Age group
    def age_group(row):
        if row['Date of Birth'] == '':
            raise Exception("{GivenNames} {Surname} does not have a date of birth.".format(GivenNames=row['Given Names'], Surname=row['Surname']))
        dob = datetime.strptime(row['Date of Birth'], '%d/%m/%Y')
        if row['Date of Death'] == '':
            raise Exception("{GivenNames} {Surname} does not have a date of death.".format(GivenNames=row['Given Names'], Surname=row['Surname']))
        dod = datetime.strptime(row['Date of Death'], '%d/%m/%Y')
        # A bool that represents if today's day/month precedes the birth day/month
        one_or_zero = ((dod.month, dod.day) < (dob.month, dob.day))
        # Calculate the difference in years from the date object's components
        year_difference = dod.year - dob.year     
        age_years = year_difference - one_or_zero
        age_days = (dod - dob).days
        age_group = ''
        if age_years >= 18:
            raise Exception("{GivenNames} {Surname} appears to be an adult aged {Age} years.\nPlease review this case before re-uploading the BDM list.".format(GivenNames=row['Given Names'], Surname=row['Surname'], Age=age_years)) # Raise an exception if an adult case is detected
        elif age_years >= 15:
            age_group = '15 to 17 years'
        elif age_years >= 10:
            age_group = '10 to 14 years'
        elif age_years >= 5:
            age_group = '5 to 9 years'
        elif age_years >= 1:
            age_group = '1 to 4 years'
        elif age_days > 28:
            age_group = '1 to 11 months'
        elif age_days < 28:
            age_group = '< 28 days'
        elif not age_days:
            age_group = ''
        return age_group
     
    df['age_group'] = df.apply(lambda row: age_group(row), axis=1)
    
    df['year_of_death'] = df.apply(lambda x: str(datetime.strptime(x['Date of Death'], '%d/%m/%Y').year), axis=1)
    
    # Process cause of death
    cod_fields = ["Cause of Death 1B", "Cause of Death 1C", "Cause of Death 1D", "Cause of Death 1E", "Cause of Death 2A", "Cause of Death 2B", "Cause of Death 2C", "Cause of Death 2D", "Cause of Death 2E"]
    def cause_of_death(row): # function to concatenate cod fields that have values
        cause = row['Cause of Death 1A']
        for field in cod_fields:
            if row[field] != "":
                cause = cause + "; " + row[field]
        return cause
    
    df['cause_of_death'] = df.apply(cause_of_death, axis=1) # apply the function
    df.drop(df.columns.to_series()['Cause of Death 1A':'Cause of Death 2F Units'], axis=1, inplace=True) # drop the fields
    
    # Process address and country of birth fields
    df['address'] = df.apply(lambda row: row['Residential Address 1'].split(',')[0].title(), axis=1)
    df['suburb'] = df.apply(lambda row: row['Residential Address 2'].split(row['State'])[0].title(), axis=1)
    df['Postcode'] = df.apply(lambda row: '0' + row['Postcode'] if len(row['Postcode']) == 3 else row['Postcode'], axis=1)
    df['residential_status'] = df['State'].apply(lambda x: 'SA' if x == 'SA' else 'Outside SA' if x in ['QLD','NSW','ACT','VIC','TAS','NT','WA'] else 'Outside Australia')

    # Process SEIFA, regions and remoteness (ARIA)
    with open('nested_dict.txt') as dict_file: 
        nested_dict = json.load(dict_file)
    with open('regions.txt') as dict_file:
        regions_dict = json.load(dict_file)
    with open('aria_dict.txt') as dict_file:
        aria_dict = json.load(dict_file)
        
    def seifa_region_aria(data):
        df = data.copy(deep=True)
        for i, row in df.iterrows():
            if row['Postcode']:
                year_of_death = int(row['year_of_death'])
                postcode = row['Postcode']
                census_year = ''
                if year_of_death >= 2014:
                    census_year = '2016'
                elif year_of_death < 2014 and year_of_death >= 2009:
                    census_year = '2011'
                elif year_of_death < 2009:
                    census_year = '2006'
                df.at[i, 'seifa_disadvantage'] = str(nested_dict[census_year][postcode]['SEIFA_disadvantage'])
                df.at[i, 'seifa_adv_disadv'] = str(nested_dict[census_year][postcode]['SEIFA_advantage_disadvantage'])
                df.at[i, 'seifa_education_occupation'] = str(nested_dict[census_year][postcode]['SEIFA_education_occupation'])
                df.at[i, 'seifa_economic_resources'] = str(nested_dict[census_year][postcode]['SEIFA_economic'])
                df.at[i, 'remoteness_area'] = aria_dict[census_year][postcode]
                if row['residential_status'] == 'SA':
                    df.at[i, 'region'] = regions_dict[postcode]
                else:
                    df.at[i, 'region'] = ''
        return df
    
    df = seifa_region_aria(df)
        
    # Process countries of birth
    aus_patterns = ["AUSTRALIA","VIC","VICTORIA","NSW","NEW SOUTH WALES","ACT","CAPITAL TERRITORY","TAS","TASMANIA","QLD","QUEENSLAND","WESTERN AUSTRALIA","NORTHERN TERRITORY"]
    df['country_of_birth'] = df.apply(lambda row: 'AUSTRALIA' if any(x in row['Place Of Birth'].upper() for x in aus_patterns) else row['Place Of Birth'].split(', ')[-1], axis=1)
    df['father_country_of_birth'] = df.apply(lambda row: 'AUSTRALIA' if any(x in row['Father Place of Birth'].upper() for x in aus_patterns) else row['Father Place of Birth'].split(', ')[-1], axis=1)
    df['mother_country_of_birth'] = df.apply(lambda row: 'AUSTRALIA' if any(x in row['Mother Place of Birth'].upper() for x in aus_patterns) else row['Mother Place of Birth'].split(', ')[-1], axis=1)
    countries_dict = {'Australia': 1101, 'Norfolk Island': 1102, 'Australian External Territories, nec': 1199, 'New Zealand': 1201, 'New Caledonia': 1301, 'Papua New Guinea': 1302, 'Solomon Islands': 1303, 'Vanuatu': 1304, 'Guam': 1401, 'Kiribati': 1402, 'Marshall Islands': 1403, 'Micronesia, Federated States of': 1404, 'Nauru': 1405, 'Northern Mariana Islands': 1406, 'Palau': 1407, 'Cook Islands': 1501, 'Fiji': 1502, 'French Polynesia': 1503, 'Niue': 1504, 'Samoa': 1505, 'Samoa, American': 1506, 'Tokelau': 1507, 'Tonga': 1508, 'Tuvalu': 1511, 'Wallis and Futuna': 1512, 'Pitcairn Islands': 1513, 'Polynesia (excludes Hawaii), nec': 1599, 'Adelie Land (France)': 1601, 'Argentinian Antarctic Territory': 1602, 'Australian Antarctic Territory': 1603, 'British Antarctic Territory': 1604, 'Chilean Antarctic Territory': 1605, 'Queen Maud Land (Norway)': 1606, 'Ross Dependency (New Zealand)': 1607, 'England': 2102, 'Isle of Man': 2103, 'Northern Ireland': 2104, 'Scotland': 2105, 'Wales': 2106, 'Guernsey': 2107, 'Jersey': 2108, 'Ireland': 2201, 'Austria': 2301, 'Belgium': 2302, 'France': 2303, 'Germany': 2304, 'Liechtenstein': 2305, 'Luxembourg': 2306, 'Monaco': 2307, 'Netherlands': 2308, 'Switzerland': 2311, 'Denmark': 2401, 'Faroe Islands': 2402, 'Finland': 2403, 'Greenland': 2404, 'Iceland': 2405, 'Norway': 2406, 'Sweden': 2407, 'Aland Islands': 2408, 'Andorra': 3101, 'Gibraltar': 3102, 'Holy See': 3103, 'Italy': 3104, 'Malta': 3105, 'Portugal': 3106, 'San Marino': 3107, 'Spain': 3108, 'Albania': 3201, 'Bosnia and Herzegovina': 3202, 'Bulgaria': 3203, 'Croatia': 3204, 'Cyprus': 3205, 'North Macedonia': 3206, 'Greece': 3207, 'Moldova': 3208, 'Romania': 3211, 'Slovenia': 3212, 'Montenegro': 3214, 'Serbia': 3215, 'Kosovo': 3216, 'Belarus': 3301, 'Czechia': 3302, 'Estonia': 3303, 'Hungary': 3304, 'Latvia': 3305, 'Lithuania': 3306, 'Poland': 3307, 'Russian Federation': 3308, 'Slovakia': 3311, 'Ukraine': 3312, 'Algeria': 4101, 'Egypt': 4102, 'Libya': 4103, 'Morocco': 4104, 'Sudan': 4105, 'Tunisia': 4106, 'Western Sahara': 4107, 'Spanish North Africa': 4108, 'South Sudan': 4111, 'Bahrain': 4201, 'Gaza Strip and West Bank': 4202, 'Iran': 4203, 'Iraq': 4204, 'Israel': 4205, 'Jordan': 4206, 'Kuwait': 4207, 'Lebanon': 4208, 'Oman': 4211, 'Qatar': 4212, 'Saudi Arabia': 4213, 'Syria': 4214, 'Turkey': 4215, 'United Arab Emirates': 4216, 'Yemen': 4217, 'Myanmar': 5101, 'Cambodia': 5102, 'Laos': 5103, 'Thailand': 5104, 'Vietnam': 5105, 'Brunei Darussalam': 5201, 'Indonesia': 5202, 'Malaysia': 5203, 'Philippines': 5204, 'Singapore': 5205, 'Timor-Leste': 5206, 'China': 6101, 'Hong Kong': 6102, 'Macau': 6103, 'Mongolia': 6104, 'Taiwan ': 6105, 'Japan': 6201, 'North Korea': 6202, 'South Korea': 6203, 'Bangladesh': 7101, 'Bhutan': 7102, 'India': 7103, 'Maldives': 7104, 'Nepal': 7105, 'Pakistan': 7106, 'Sri Lanka': 7107, 'Afghanistan': 7201, 'Armenia': 7202, 'Azerbaijan': 7203, 'Georgia': 7204, 'Kazakhstan': 7205, 'Kyrgyzstan': 7206, 'Tajikistan': 7207, 'Turkmenistan': 7208, 'Uzbekistan': 7211, 'Bermuda': 8101, 'Canada': 8102, 'St Pierre and Miquelon': 8103, 'United States of America': 8104, 'Argentina': 8201, 'Bolivia': 8202, 'Brazil': 8203, 'Chile': 8204, 'Colombia': 8205, 'Ecuador': 8206, 'Falkland Islands': 8207, 'French Guiana': 8208, 'Guyana': 8211, 'Paraguay': 8212, 'Peru': 8213, 'Suriname': 8214, 'Uruguay': 8215, 'Venezuela': 8216, 'South America, nec': 8299, 'Belize': 8301, 'Costa Rica': 8302, 'El Salvador': 8303, 'Guatemala': 8304, 'Honduras': 8305, 'Mexico': 8306, 'Nicaragua': 8307, 'Panama': 8308, 'Anguilla': 8401, 'Antigua and Barbuda': 8402, 'Aruba': 8403, 'Bahamas': 8404, 'Barbados': 8405, 'Cayman Islands': 8406, 'Cuba': 8407, 'Dominica': 8408, 'Dominican Republic': 8411, 'Grenada': 8412, 'Guadeloupe': 8413, 'Haiti': 8414, 'Jamaica': 8415, 'Martinique': 8416, 'Montserrat': 8417, 'Puerto Rico': 8421, 'St Kitts and Nevis': 8422, 'St Lucia': 8423, 'St Vincent and the Grenadines': 8424, 'Trinidad and Tobago': 8425, 'Turks and Caicos Islands': 8426, 'Virgin Islands, British ': 8427, 'Virgin Islands': 8428, 'St Barthelemy': 8431, 'St Martin': 8432, 'Bonaire, Sint Eustatius and Saba': 8433, 'Curacao': 8434, 'Sint Maarten': 8435, 'Benin': 9101, 'Burkina Faso': 9102, 'Cameroon': 9103, 'Cabo Verde': 9104, 'Central African Republic': 9105, 'Chad': 9106, 'Congo, Republic of': 9107, 'Congo, Democratic Republic of': 9108, "Cote d'Ivoire": 9111, 'Equatorial Guinea': 9112, 'Gabon': 9113, 'Gambia': 9114, 'Ghana': 9115, 'Guinea': 9116, 'Guinea-Bissau': 9117, 'Liberia': 9118, 'Mali': 9121, 'Mauritania': 9122, 'Niger': 9123, 'Nigeria': 9124, 'Sao Tome and Principe': 9125, 'Senegal': 9126, 'Sierra Leone': 9127, 'Togo': 9128, 'Angola': 9201, 'Botswana': 9202, 'Burundi': 9203, 'Comoros': 9204, 'Djibouti': 9205, 'Eritrea': 9206, 'Ethiopia': 9207, 'Kenya': 9208, 'Lesotho': 9211, 'Madagascar': 9212, 'Malawi': 9213, 'Mauritius': 9214, 'Mayotte': 9215, 'Mozambique': 9216, 'Namibia': 9217, 'Reunion': 9218, 'Rwanda': 9221, 'St Helena': 9222, 'Seychelles': 9223, 'Somalia': 9224, 'South Africa': 9225, 'Eswatini': 9226, 'Tanzania': 9227, 'Uganda': 9228, 'Zambia': 9231, 'Zimbabwe': 9232, 'Southern and East Africa, nec': 9299}
    df['cald_source_details'] = ""
    
    def country_of_birth(data):
        df = data.copy(deep=True)
        cob_fields = ['country_of_birth','father_country_of_birth','mother_country_of_birth']
        for i, row in df.iterrows():
            for field in cob_fields:
                if row[field] != "":
                    if row[field].title() in countries_dict.keys():
                        df.at[i, field] = countries_dict[row[field].title()]
                    else:
                        for country in countries_dict.keys():
                            country_cap = country.upper()
                            if row[field] == country_cap:
                                df.at[i, field] = countries_dict[country]
                                break
                            elif row[field].split(" ")[-1].upper() in country_cap and row[field].split(" ")[0].upper() in country_cap:
                                df.at[i, field] = countries_dict[country]
                                break
                    # If country not found, assign empty string (null)
                    if isinstance(df.at[i, field], str):
                        df.at[i, field] = ""
                        if field == 'country_of_birth':
                            df.at[i, 'cald_source_details'] += "Country of birth was not successfully parsed when imported from BDM list. See the 'Place of birth' field on the Case information form for the raw data.\r"
                        elif field == 'father_country_of_birth':
                            df.at[i, 'cald_source_details'] += "Father's country of birth was not successfully parsed when imported from BDM list. See the 'father_place_of_birth' field available in data exports and reports for the raw data.\r"
                        elif field == 'mother_country_of_birth':
                            df.at[i, 'cald_source_details'] += "Mother's country of birth was not successfully parsed when imported from BDM list. See the 'mother_place_of_birth' field available in data exports and reports for the raw data.\r"
        return df
    
    df = country_of_birth(df)
    
    
    # Process life duration
    df['life_duration_minutes'] = df.apply(lambda row: str(int(row['Age'])*60) if (row['Age Units'] == "HOURS" and int(row['Age']) < 24) or row['Age Units'] == "HOUR" else (str(row['Age']) if row['Age Units'] == "MINUTES" else ""), axis=1)
    
    # Process Aboriginal status
    df['cultural_background'] = df.apply(lambda row: 2 if (row['Aboriginal Indicator'] == 'Y' or row['Torres Strait Islander Indicator'] == 'Y') else 1, axis=1)
    
    # Drop unneeded fields
    df.drop(['Residential Address 1',
             'Residential Address 2',
             'Aboriginal Indicator',
             'Torres Strait Islander Indicator',
             'Age',
             'Age Units',
             'Place of Death 2',
             'Doctors Address 2'],
            axis=1, inplace=True)
    
    # Rename fields
    df.rename(columns={
        'Reg No': 'bdm_id',
        'Date Registered': 'bdm_date_of_registration',
        'Surname': 'surname',
        'Given Names': 'given_names',
        'Postcode': 'postcode',
        'State': 'state',
        'Date of Birth': 'dob',
        'Date of Death': 'dod',
        'Place Of Birth': 'place_of_birth',
        'Sex': 'sex',
        'Coroner Indicator': 'coronial',
        'Period of Residence': 'period_of_residence',
        'Place of Death 1': 'place_of_death',
        'Surname of Father': 'father_surname',
        'Surname of Father at Birth': 'father_alias',
        'Given Names of Father': 'father_givenname',
        'Father DOB': 'father_dob',
        'Father Place of Birth': 'father_place_of_birth',
        'Father Period of Residence': 'father_period_of_residence',
        'Surname of Mother': 'mother_surname',
        'Surname of Mother at Birth': 'mother_alias',
        'Given Names of Mother': 'mother_givenname',
        'Mother DOB': 'mother_dob',
        'Mother Place of Birth': 'mother_place_of_birth',
        'Mother Period of Residence': 'mother_period_of_residence',
        'Doctors Name': 'doctor_name',
        'Doctors Address 1': 'doctor_location'   
        }, inplace=True)
    
    df = df.astype(str)
    
    # Convert places to title case
    exceptions = ['SA','NSW','WA','ACT','NT','VIC','QLD','TAS','FMC','WCH','AVE','ST','TCE','RD','OF','AND']

    def title_except(s, exceptions):
        word_list = re.split(' ', s)       # re.split behaves as expected
        final = [word_list[0].capitalize() if word_list[0] not in exceptions else word_list[0]]
        for word in word_list[1:]:
            final.append(word.lower() if word in exceptions else word.capitalize())
        return " ".join(final)
    
    
    for col in ['place_of_birth','father_place_of_birth','mother_place_of_birth','place_of_death','doctor_location']:
        for i, row in df.iterrows():
            df.at[i, col] = title_except(row[col], exceptions)


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
    
    
    # Assign family CALD status       
    fields = ['country_of_birth','mother_country_of_birth','father_country_of_birth']

    def family_cald_status(data):
        df = data.copy(deep=True)
        df['parents_cald_background'] = ''
        
        for i, row in df.iterrows():
            if all(row[field] > '1101' for field in fields):
                df.at[i, 'parents_cald_background'] = '1' # Child and both parents born overseas 
            elif row['country_of_birth'] > '1101' and row['mother_country_of_birth'] == '' and row['father_country_of_birth'] == '':
                df.at[i, 'parents_cald_background'] = '2' # Child born overseas and no information on parents
            elif row['country_of_birth'] == '1101' and row['mother_country_of_birth'] > '1101' and row['father_country_of_birth'] > '1101':
                df.at[i, 'parents_cald_background'] = '3' # Both parents born overseas and child born in Aus
            elif row['country_of_birth'] == '1101' and any(row[parent] > '1101' for parent in ['mother_country_of_birth','father_country_of_birth']) and any(row[parent] == '1101' for parent in ['mother_country_of_birth','father_country_of_birth']):
                df.at[i, 'parents_cald_background'] = '4' # One parent born overseas and child born in Aus
            elif row['country_of_birth'] > '1101' and all(row[parent] == '1101' for parent in ['mother_country_of_birth','father_country_of_birth']):
                df.at[i, 'parents_cald_background'] = '5' # Child born overseas and parents born in Aus
            elif row['country_of_birth'] == '1101' and any(row[parent] == '' for parent in ['mother_country_of_birth','father_country_of_birth']) and all(row[parent] <= '1101' for parent in ['mother_country_of_birth','father_country_of_birth']):
                df.at[i, 'parents_cald_background'] = '6' # Child born in Aus and no information on 1 or 2 parents (no parents born overseas)
            elif all(row[field] == '1101' for field in fields):
                df.at[i, 'parents_cald_background'] = '7' # Child and parents born in Aus
            elif all(row[field] == '' for field in fields):
                df.at[i, 'parents_cald_background'] = '9' #Unknown
            else:
                df.at[i, 'parents_cald_background'] = '8' # Other not fitting into categories 1-7
        
        return df
    
    df = family_cald_status(df)
    
    # CALD status
    def cald_status(row):
        cald_background = ''
        if all(row[field] == '1101' for field in fields):
            cald_background = '2' # Not CALD (No)
        elif any(row[field] > '1101' for field in fields):
            cald_background = '1' # CALD (Yes)
        else:
            cald_background = '0' # Unknown (update during screening)
        return cald_background
    
    df['cald'] = df.apply(lambda x: cald_status(x), axis=1)
    
    # Assign default values since these aren't processed by REDCap when importing data
    df['screening_status'] = '1'
    df['review_status'] = '1' #both pending
    df['information_available___0'] = '1' #None
    df['category_of_death'] = '0' #pending
    df['cp_history'] = '0' #not checked
    df['disability_register'] = '0' #pending
    
    # The interface
    st.download_button('Download CSV', df.to_csv().encode('utf-8'), bdm_list.name[:-4]+'_processed.csv', 'text/csv')
    
    st.subheader("Preview data")
    st.write(df)


