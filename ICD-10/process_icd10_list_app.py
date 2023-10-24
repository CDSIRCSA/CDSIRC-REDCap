# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import msoffcrypto
import io
import re
import streamlit as st


st.title('ICD-10 list to REDCap converter')

# User selects a file
file = st.file_uploader(label='Upload an ICD-10 coding list (.xlsx)',
                            type=['xlsx'])
if file:
    
    # Decrypt the file
    temp = io.BytesIO()
    
   excel = msoffcrypto.OfficeFile(file)
   excel.load_key('jazzy')
   excel.decrypt(temp)
    
    # Load it into a df
    df = pd.read_excel(temp, dtype=str)
    del temp
    
    df.columns = [x.strip() for x in df.columns] #remove leading space from column names
    df.replace({np.nan:''}, inplace=True) #replace nans
    
    # Rename the columns for REDCap
    df.rename(columns={'Case Number':'case_number',
                       'Place of occurrence code':'place_code',
                       'Activity code':'activity_code',
                       'NCHIRT comments':'icd_coder_comments',
                       'SA CDSIRC Response':'response_to_coder',
                       'ICD-10 Underlying Cause of Death':'underlying_cod',
                       'ICD-10 MCOD 1a)':'mcod_1a_1',
                       'ICD-10 MCOD 1b)':'mcod_1b_1',
                       'ICD-10 MCOD 1c)':'mcod_1c',
                       'ICD-10 MCOD 1d)':'mcod_1d',
                       'ICD-10 MCOD 2':'mcod_2',
                       'ICD-10 P 1a) Main Fetal Condition':'main_fetal_condition_1',
                       'ICD-10 P 1b) Other Fetal Conditions':'other_fetal_conditions_1',
                       'ICD-10 P 1c) Main Maternal Condition':'main_maternal_condition',
                       'ICD-10 P 1d) Other Maternal Conditions':'other_maternal_conditions_1',
                       'ICD-10 P 2 Other relevant circumstances':'other_rel_circumstances'}, inplace=True)
    
    # --------------------------------------
    # Split the codes into separate REDCap fields
    res = df['mcod_1a_1'].str.replace('[\s+]', '', regex=True).str.split(',', expand=True).iloc[:,0:3]
    if len(res.columns) < 3:
        while len(res.columns) < 3:
            res[len(res.columns)+1] = ''
    df[['mcod_1a_1','mcod_1a_2','mcod_1a_3']] = res
    
    res = df['mcod_1b_1'].str.replace('[\s+]', '', regex=True).str.split(',', expand=True).iloc[:,0:3]
    if len(res.columns) < 3:
        while len(res.columns) < 3:
            res[len(res.columns)+1] = ''
    df[['mcod_1b_1','mcod_1b_2','mcod_1b_3']] = res
    
    df['mcod_1c'] = df['mcod_1c'].str.split(',', expand=True).iloc[:,0]
    
    df['mcod_1d'] = df['mcod_1d'].str.split(',', expand=True).iloc[:,0]
    
    df['mcod_2'] = df['mcod_2'].str.split(',', expand=True).iloc[:,0]
    
    res = df['main_fetal_condition_1'].str.replace('[\s+]', '', regex=True).str.split(',', expand=True).iloc[:,0:3]
    if len(res.columns) < 3:
        while len(res.columns) < 3:
            res[len(res.columns)+1] = ''
    df[['main_fetal_condition_1','main_fetal_condition_2','main_fetal_condition_3']] = res
    
    res = df['other_fetal_conditions_1'].str.replace('[\s+]', '', regex=True).str.split(',', expand=True).iloc[:,0:3]
    if len(res.columns) < 3:
        while len(res.columns) < 3:
            res[len(res.columns)+1] = ''
    df[['other_fetal_conditions_1','other_fetal_conditions_2','other_fetal_conditions_3']] = res
    
    df['main_maternal_condition'] = df['main_maternal_condition'].str.split(',', expand=True).iloc[:,0]
    
    res = df['other_maternal_conditions_1'].str.replace('[\s+]', '', regex=True).str.split(',', expand=True).iloc[:,0:2]
    if len(res.columns) < 2:
        while len(res.columns) < 2:
            res[len(res.columns)+1] = ''
    df[['other_maternal_conditions_1','other_maternal_conditions_2']] = res
    
    df['other_rel_circumstances'] = df['other_rel_circumstances'].str.split(',', expand=True).iloc[:,0]
    
    
    # --------------------------------------
    # Add missing periods to codes and remove leading whitespace
    code_fields = ['underlying_cod','mcod_1a_1','mcod_1a_2','mcod_1a_3','mcod_1b_1','mcod_1b_2','mcod_1b_3','mcod_1c','mcod_1d','mcod_2','main_fetal_condition_1','main_fetal_condition_2','main_fetal_condition_3','other_fetal_conditions_1','other_fetal_conditions_2','other_fetal_conditions_3','main_maternal_condition','other_maternal_conditions_1','other_maternal_conditions_2','other_rel_circumstances']
    invalid_codes = []
    for i, row in df.iterrows():
        for field in code_fields:
            if row[field]:
                if row[field][0] == ' ': # if leading space, remove space
                    df.at[i, field] = row[field][1:]
                elif bool(re.match(r'\D\d', row[field])): # if the code starts with a letter then a number
                    if len(row[field]) > 3 and row[field][3] != '.': # if it's missing a period
                        df.at[i, field] = row[field][0:3] + '.' + row[field][-1] # add the period
                else: # add to invalid codes list
                    invalid_codes.append('- Case {} ({}): \'{}\''.format(row['case_number'], field, row[field]))
    
    # --------------------------------------
    # Select fields to keep and remove None values
    df = df[['case_number','underlying_cod','mcod_1a_1','mcod_1a_2','mcod_1a_3','mcod_1b_1','mcod_1b_2','mcod_1b_3','mcod_1c','mcod_1d','mcod_2','main_fetal_condition_1','main_fetal_condition_2','main_fetal_condition_3','other_fetal_conditions_1','other_fetal_conditions_2','other_fetal_conditions_3','main_maternal_condition','other_maternal_conditions_1','other_maternal_conditions_2','other_rel_circumstances','place_code', 'activity_code','icd_coder_comments','response_to_coder']]
    df.set_index('case_number', inplace=True)
    df.replace({None:''}, inplace=True)
    # Assign coding status
    df['coding_status'] = df.apply(lambda x: '4' if x['underlying_cod'] != '' and x['icd_coder_comments'] == '' else '3', axis=1)
    
    # --------------------------------------
    # Download the data
    st.download_button('Download processed data', df.to_csv().encode('utf-8'), file.name[:-5]+'_processed.csv', 'text/csv')
    
    if len(invalid_codes) > 0:
        st.subheader("Errors")
        st.write("Please fix or remove the following invalid codes before loading into REDCap:")
        st.write('\n'.join(invalid_codes))
    
    st.subheader("Preview data")
    st.write(df)
