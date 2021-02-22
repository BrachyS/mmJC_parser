
#!/usr/bin/python

""" This module contains functions that load raw data, reformat data, handling missing data and outliers"""


import pandas as pd
import numpy as np
import sys



filename1 = 'data/raw/mmJC_020521.csv'

filename2 = 'data/raw/mmJC_020521_meta.csv'

# Read in data files
def import_data(filename1,filename2):
    """Read in records and meta data"""
    raw = pd.read_csv('data/raw/mmJC_020521.csv',
                      na_values = {"Probe":"UNKNOWN"})

    meta = pd.read_csv(filename2)
    meta.columns = ['station_name','treatment']

    return raw, meta




# Add TimeDelta and reshape records data (i.e.,raw)
def raw_reshape(raw):
    """Add TimeDelta and reshape records data  """

    raw['TimeDelta'] = pd.to_timedelta(raw['Hours'], unit='h')

    # Reshape data and drop missing values
    df_long = pd.melt(raw, id_vars=['Probe', 'Hours', 'TimeDelta'],
                      var_name='id',
                      value_name='records').dropna(how='any')

    # Set TimeDelta to index and be sure records are float
    df_long = df_long.set_index('TimeDelta')


    return df_long



def remove_var(df_long, variable = 'LH'):
    """Remove a variable (e.g.,Liquid handling) from dataframe and store in a separate table.
    In addition, Convert records to numeric type"""

    df_clean = df_long.copy()
    sub_df = df_clean[df_clean.id.str.contains(variable)]
    df_clean = df_clean[~df_clean.id.str.contains(variable)]

    # convert records in df_long to numeric
    df_clean['records'] = df_clean['records'].apply(pd.to_numeric)

    return sub_df, df_clean



# Add columns for chamber, location and variable
def add_columns(df_long):
    """Add columns for chamber, location and variable"""

    df_long[['loc', 'chamber', 'variable']] = df_long.id.str.split('-', expand=True)
    df_long['station_id'] = df_long['loc'] + '-' + df_long['chamber']

    return df_long

