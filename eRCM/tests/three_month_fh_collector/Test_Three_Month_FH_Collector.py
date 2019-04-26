import os
import sys
import pandas as pd
import datetime
import numpy as np

# setup library dict in the studio style
libraries = {'numpy': np, 'pandas': pd, 'datetime': datetime}

# set the script path for module import
script_path = os.path.abspath(os.path.join("__file__", "../../../scripts"))
sys.path.append(script_path)

# import modules for testing
from Three_Month_FH_Collector import limit_data_set, calc_monthly_values, calc_windows, calc_rolling_avg


def test(lib):
    """
    Args:
        lib: dictionary of libraries; access by name
        e.g. pd = libraries['pandas'] or stats = libraries['scipy']['stats']

    Returns:
        whether or not calculated data frame matches the answer
    """
    pd = lib['pandas']
    datetime = lib['datetime']
    np = lib['numpy']

    period = 3
    date_selection = 'Last_Record'

    test_data = pd.read_csv('tmfhc.csv', parse_dates=['Depart_Date'])
    answer = pd.read_csv('tmfhcA.csv', parse_dates=['Three_Month_Start_Date'])

    # call the relevant functions
    ldf, last_date = limit_data_set(test_data, date_selection, libraries)
    tot = calc_monthly_values(ldf, libraries)
    win = calc_windows(tot, period, libraries)
    fin = calc_rolling_avg(win, last_date, period, libraries)

    # drop the first two records off each data set to compensate for data cutoff values
    fin = fin.iloc[2:]
    answer = answer.iloc[2:]

    # assert that the data frames are equal
    pd.testing.assert_frame_equal(fin, answer)


test(libraries)
