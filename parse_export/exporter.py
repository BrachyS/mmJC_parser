#!/usr/bin/python
""" This module output data as:
    1) an excel file easy for plotting
    2) a set of csv files correponding to a database schema to store/query data"""

import pandas as pd
import numpy as np
import sys


# Parse data by variables, remove majority of missing values and output into excel

def long_to_wide_excel(df_long, freq = '1H', filepath = '../data/processed/1H_mean.xlsx'):
    """Export wide format file to excel

    :param df_long: long-format data file to be transformed
    :param freq: frequency to downsample time intervals, default to 1 hour
    :param filepath: path to store resulted file

    :return: an Excel file with multiple sheets, each store records for one variable"""

    variables = list(df_long['variable'].unique())

    with pd.ExcelWriter(filepath, datetime_format='hh:mm:ss.000') as writer:

        # Write each variable data to an Excel sheet

        # After processing, these data frames have much fewer missing values than the raw data,
        # and share same timestamp across chambers and variables
        for var in variables:
            subset = df_long.loc[df_long['variable'] == var, ['station_id', 'records']]

            # reshape data into wide form
            subset_wide = subset.pivot_table(index='TimeDelta', values='records', columns='station_id')

            # Downsample data to 1 hour, taking averages, then drop rows in which all chambers had missing data
            # There are still some missing data, and need to consult client about if necessary to remove them
            subset_1H = subset_wide.resample(freq).mean().dropna(how='all')

            subset_1H = subset_1H.reset_index()
            subset_1H['TimeDelta'] = subset_1H['TimeDelta'].astype('str') # for storing in excel file

            subset_1H.to_excel(writer, sheet_name=var)


# Export CSV files for database importer

def csv_to_db(fact1, fact2, meta, filepath):
    """Export csv files which correspond to the database schema for easy import
    :param fact1: long-format data containing variable records
    :param fact2: long-format data containing LH records
    :param meta: meta data
    :param filepath: path to store resulted files
    :return: 5 csv files"""

    ### Formating tables
    # 1. fact table 1 for variable records
    cols = ['station_id', 'Hours', 'variable', 'records']
    fact_records = fact1.reset_index()[cols]

    # 2. fact table 2 for Liquid handling
    # format LH table
    fact2[['loc', 'chamber', 'variable']] = fact2.id.str.split('-', expand=True)
    fact2['station_id'] = fact2['loc'] + '-' + fact2['chamber']
    fact2.head()

    fact_LH = fact2.reset_index()[['station_id', 'Hours', 'records']]

    # 3. dimension table for stations
    dim_stations = meta
    dim_stations.columns = ['station_name', 'treatment']

    # 4. dimension table for variables
    dim_variable = pd.DataFrame(list(fact1['variable'].unique()))
    dim_variable.columns = ['name']

    # 5. dimension table for time
    dim_time = fact1.reset_index()[['Hours', 'Probe']]

    ## Export to csv files
    fact_records.to_csv(filepath + 'fact_records.csv')
    fact_LH.to_csv(filepath + 'fact_LH.csv')
    dim_stations.to_csv(filepath + 'dim_stations.csv')
    dim_variable.to_csv(filepath + 'dim_variable.csv')
    dim_time.to_csv(filepath + 'dim_time.csv')
