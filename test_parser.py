import pytest
import pandas as pd
import numpy as np
from parse_export.parser import *
from parse_export.exporter import *

filename1 = 'data/raw/mmJC_020521.csv'
filename2 = 'data/raw/mmJC_020521_meta.csv'

def test_import_data():
    """Test if data files are appropriately imported"""


    # read in a sample of records
    raw, meta = import_data(filename1, filename2)

    assert raw.shape[0] > 0
    assert raw.shape[1] > 0
    assert meta.shape[0] > 0
    assert meta.shape[1] > 0


def test_raw_reshape():
    """Test if index and columns are correctly set"""
    # read in a sample of data
    raw = pd.read_csv(filename1, nrows=50,
                      na_values={"Probe": "UNKNOWN"})

    df = raw_reshape(raw)
    expected_cols = ['Probe', 'Hours', 'id', 'records']

    assert df.index.dtype == '<m8[ns]' # check index dtype is TimeDelta
    assert list(df.columns) == expected_cols # check columns names are correct


def test_remove_var():
    """Test if the variable is completely removed """
    # read in a sample of file containing 'LH'
    raw = pd.read_csv(filename1,
                      na_values={"Probe": "UNKNOWN"})
    df = raw_reshape(raw)

    sub_df, df_long = remove_var(df, 'LH')

    assert sum(df_long.id.str.contains('LH')) == 0

