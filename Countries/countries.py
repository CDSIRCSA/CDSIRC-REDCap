# -*- coding: utf-8 -*-
import pandas as pd

countries = "USA, United States of America|AFG, Afghanistan|ALA, Åland Islands|ALB, Albania|DZA, Algeria|ASM, American Samoa|AND, Andorra|AGO, Angola|AIA, Anguilla|ATG, Antigua and Barbuda|ARG, Argentina|ARM, Armenia|ABW, Aruba|AUS, Australia|AUT, Austria|AZE, Azerbaijan|BHS, Bahamas|BHR, Bahrain|BGD, Bangladesh|BRB, Barbados|BLR, Belarus|BEL, Belgium|BLZ, Belize|BEN, Benin|BMU, Bermuda|BTN, Bhutan|BOL, Bolivia (Plurinational State of)|BIH, Bosnia and Herzegovina|BWA, Botswana|BRA, Brazil|VGB, British Virgin Islands|BRN, Brunei Darussalam|BGR, Bulgaria|BFA, Burkina Faso|BDI, Burundi|KHM, Cambodia|CMR, Cameroon|CAN, Canada|CPV, Cape Verde|CYM, Cayman Islands|CAF, Central African Republic|TCD, Chad|CIS, Channel Islands|CHL, Chile|CHN, China|HKG, China, Hong Kong Special Administrative Region|MAC, China, Macao Special Administrative Region|COL, Colombia|COM, Comoros|COG, Congo|COK, Cook Islands|CRI, Costa Rica|CIV, Côte d'Ivoire|HRV, Croatia|CUB, Cuba|CYP, Cyprus|CZE, Czech Republic|PRK, Democratic People's Republic of Korea|COD, Democratic Republic of the Congo|DNK, Denmark|DJI, Djibouti|DMA, Dominica|DOM, Dominican Republic|ECU, Ecuador|EGY, Egypt|SLV, El Salvador|GNQ, Equatorial Guinea|ERI, Eritrea|EST, Estonia|ETH, Ethiopia|FRO, Faeroe Islands|FLK, Falkland Islands (Malvinas)|FJI, Fiji|FIN, Finland|FRA, France|GUF, French Guiana|PYF, French Polynesia|GAB, Gabon|GMB, Gambia|GEO, Georgia|DEU, Germany|GHA, Ghana|GIB, Gibraltar|GRC, Greece|GRL, Greenland|GRD, Grenada|GLP, Guadeloupe|GUM, Guam|GTM, Guatemala|GGY, Guernsey|GIN, Guinea|GNB, Guinea-Bissau|GUY, Guyana|HTI, Haiti|VAT, Holy See|HND, Honduras|HUN, Hungary|ISL, Iceland|IND, India|IDN, Indonesia|IRN, Iran (Islamic Republic of)|IRQ, Iraq|IRL, Ireland|IMN, Isle of Man|ISR, Israel|ITA, Italy|JAM, Jamaica|JPN, Japan|JEY, Jersey|JOR, Jordan|KAZ, Kazakhstan|KEN, Kenya|KIR, Kiribati|KWT, Kuwait|KGZ, Kyrgyzstan|LAO, Lao People's Democratic Republic|LVA, Latvia|LBN, Lebanon|LSO, Lesotho|LBR, Liberia|LBY, Libyan Arab Jamahiriya|LIE, Liechtenstein|LTU, Lithuania|LUX, Luxembourg|MDG, Madagascar|MWI, Malawi|MYS, Malaysia|MDV, Maldives|MLI, Mali|MLT, Malta|MHL, Marshall Islands|MTQ, Martinique|MRT, Mauritania|MUS, Mauritius|MYT, Mayotte|MEX, Mexico|FSM, Micronesia (Federated States of)|MCO, Monaco|MNG, Mongolia|MNE, Montenegro|MSR, Montserrat|MAR, Morocco|MOZ, Mozambique|MMR, Myanmar|NAM, Namibia|NRU, Nauru|NPL, Nepal|NLD, Netherlands|ANT, Netherlands Antilles|NCL, New Caledonia|NZL, New Zealand|NIC, Nicaragua|NER, Niger|NGA, Nigeria|NIU, Niue|NFK, Norfolk Island|MNP, Northern Mariana Islands|NOR, Norway|PSE, Occupied Palestinian Territory|OMN, Oman|PAK, Pakistan|PLW, Palau|PAN, Panama|PNG, Papua New Guinea|PRY, Paraguay|PER, Peru|PHL, Philippines|PCN, Pitcairn|POL, Poland|PRT, Portugal|PRI, Puerto Rico|QAT, Qatar|KOR, Republic of Korea|MDA, Republic of Moldova|REU, Réunion|ROU, Romania|RUS, Russian Federation|RWA, Rwanda|BLM, Saint-Barthélemy|SHN, Saint Helena|KNA, Saint Kitts and Nevis|LCA, Saint Lucia|MAF, Saint-Martin (French part)|SPM, Saint Pierre and Miquelon|VCT, Saint Vincent and the Grenadines|WSM, Samoa|SMR, San Marino|STP, Sao Tome and Principe|SAU, Saudi Arabia|SEN, Senegal|SRB, Serbia|SYC, Seychelles|SLE, Sierra Leone|SGP, Singapore|SVK, Slovakia|SVN, Slovenia|SLB, Solomon Islands|SOM, Somalia|ZAF, South Africa|ESP, Spain|LKA, Sri Lanka|SDN, Sudan|SUR, Suriname|SJM, Svalbard and Jan Mayen Islands|SWZ, Swaziland|SWE, Sweden|CHE, Switzerland|SYR, Syrian Arab Republic|TJK, Tajikistan|THA, Thailand|MKD, The former Yugoslav Republic of Macedonia|TLS, Timor-Leste|TGO, Togo|TKL, Tokelau|TON, Tonga|TTO, Trinidad and Tobago|TUN, Tunisia|TUR, Turkey|TKM, Turkmenistan|TCA, Turks and Caicos Islands|TUV, Tuvalu|UGA, Uganda|UKR, Ukraine|ARE, United Arab Emirates|GBR, United Kingdom of Great Britain and Northern Ireland|TZA, United Republic of Tanzania|VIR, United States Virgin Islands|URY, Uruguay|UZB, Uzbekistan|VUT, Vanuatu|VEN, Venezuela (Bolivarian Republic of)|VNM, Viet Nam|WLF, Wallis and Futuna Islands|ESH, Western Sahara|YEM, Yemen|ZMB, Zambia|ZWE, Zimbabwe"

print(countries.replace('|', '\n'))

abs_data = pd.read_excel('ABS countries.xls',
                         sheet_name = 'countries_modified',
                         usecols = "C,D",
                         skiprows = 6)

abs_data = abs_data.dropna()
abs_data = abs_data[abs_data.Countries.apply(lambda x: isinstance(x, int))]

for index, row in abs_data.iterrows():
    print(str(row.values[0]) + ", " + row.values[1])

abs_groups = pd.read_excel('ABS countries.xls',
                                 sheet_name = 'minor_groups')
groups_dict_manual = {1: {'name': 'Oceania and Antarctica',
                          'codes': {11: 'Australia (includes External Territories)', 12: 'New Zealand', 13: 'Melanesia', 14: 'Micronesia', 15: 'Polynesia (excludes Hawaii)', 16: 'Antarctica'}},
                      2: {'name': 'North-West Europe',
                          'codes': {21: 'United Kingdom, Channel Islands and Isle of Man', 22: 'Ireland', 23: 'Western Europe', 24: 'Northern Europe'}},
                      3: {'name': 'Southern and Eastern Europe',
                          'codes': {31: 'Southern Europe', 32: 'South Eastern Europe', 33: 'Eastern Europe'}},
                      4: {'name': 'North Africa and the Middle East',
                          'codes': {41: 'North Africa', 42: 'Middle East'}},
                      5: {'name': 'South-East Asia',
                          'codes': {51: 'Mainland South-East Asia', 52: 'Maritime South-East Asia'}},
                      6: {'name': 'North-East Asia',
                          'codes': {61: 'Chinese Asia (includes Mongolia)', 62: 'Japan and the Koreas'}},
                      7: {'name': 'Southern and Central Asia',
                          'codes': {71: 'Southern Asia', 72: 'Central Asia'}},
                      8: {'name': 'Americas',
                          'codes': {81: 'Northern America', 82: 'South America', 83: 'Central America', 84: 'Caribbean'}},
                      9: {'name': 'Sub-Saharan Africa',
                          'codes': {91: 'Central and West Africa', 92: 'Southern and East Africa'}}}
         

groups_dict = {}
for index, row in abs_groups.iterrows():
    groups_dict[row.values[0]] = {}
    groups_dict[row.values[0]][row.values[1]] = {}
    
    
for index, row in abs_groups.iterrows():
    groups_dict[row.values[0]][row.values[1]][row.values[2]] = row.values[3]

countries_dict = {}
for index, row in abs_data.iterrows():
    countries_dict[row.values[1]] = row['Countries']
