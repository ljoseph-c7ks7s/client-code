# import modules for testing
from Three_Month_FH_Collector import limit_data_set, calc_windows, calc_rolling_avg


# import libraries in dictionary style
import pandas as pd
import datetime
import numpy as np

libraries = {'numpy': np, 'pandas': pd, 'datetime': datetime}


def test(lib):
    """
    Args:
        lib: dictionary of libraries; access by name
        e.g. pd = libraries['pandas'] or stats = libraries['scipy']['stats']

    Returns:
        whether or not calculated data frame matches the answer
    """
    pd = libraries['pandas']

    period = 3
    date_selection = 'Last_Record'

    test_data = pd.read_csv('tmfhc.csv', parse_dates=['Depart_Date'])
    answer = pd.read_csv('tmfhcA.csv', parse_dates=['Three_Month_Start_Date'])

    df, last_date = limit_data_set(test_data, date_selection, lib)
    win = calc_windows(df, period, lib)
    fin = calc_rolling_avg(win, last_date, period, lib)

    # drop the first two records off each data set to compensate for dat cutoff values
    fin = fin.iloc[2:]
    answer = answer.iloc[2:]

    # assert that the data frames are equal
    pd.testing.assert_frame_equal(fin, answer)


test(libraries)
