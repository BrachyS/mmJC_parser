#!/usr/bin/python
""" This is a sample run of the software,
    It will load pre-specified raw data, remove majority of missing values and outliers,
    then output data as
    1) an excel file easy for plotting
    2) a set of csv files correponding to a database schema to store/query data"""

import pandas as pd
import numpy as np
import sys
from parse_export.parser import *
from parse_export.exporter import *



filename1 = 'data/raw/mmJC_020521.csv'

filename2 = 'data/raw/mmJC_020521_meta.csv'

# Ensure filepaths are correct
try:
    f = open(filename1)
except IOError:
    print("File %s does not exist !!" % filename1)

try:
    f = open(filename2)
except IOError:
    print("File %s does not exist !!" % filename2)


##### Parse files ######

# 1) Read in data files
print("Read in data files, output dataframes 'raw','meta'")
raw,meta = import_data(filename1, filename2)



# 2) Add TimeDelta and reshape records data
print('Add TimeDelta as Index and reshape records data into long shape, output df: df_long')
df_long= raw_reshape(raw)


# 3) Remove variable LH which contains text
# and remove majority of missing data
print('Remove variable LH which contains text and remove majority of missing data, \noutput df: LH, df_clean')
LH, df_clean = remove_var(df_long, variable = 'LH')


# 4) Remove outlier values (100000000)
# Future steps: we could write a function and adopt a criteria to systematically remove outliers
# Will need to consult the client about specific criteria, for example, 1.5*IQR
print('Removed outliers - values > 10000')
df_clean = df_clean.loc[df_clean['records'] < 10000,:]


# 4) Add columns for chamber, location and variable
print('Add columns for chamber, location and variable')
df_clean = add_columns(df_clean)



##### Export files ######

# 1) Export wide format to excel file

# Export 1 hour means
print('Exporting Excel file...')
long_to_wide_excel(df_clean, freq = '1H', filepath = 'data/processed/1H_mean.xlsx')

# 2 ) Export csv files for database
print('Exporting csv files...')
csv_to_db(df_clean, LH, meta, filepath= 'data/processed/db/')

print('All done! ')