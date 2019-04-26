# import libraries in dictionary style
import pandas as pd

# import modules for testing
from Domain_Check import domain_check

# create libraries dict in studio fashion
libraries = {'pandas': pd}


def test(lib):
    """
    Args:
        lib: dictionary of libraries; access by name
        e.g. pd = libraries['pandas'] or stats = libraries['scipy']['stats']

    Returns:
        whether or not calculated data frame matches the answer
    """
    pd = lib['pandas']

    # import data for testing
    tmfh_data = pd.read_csv('tmfh_sample.csv', parse_dates=['Three_Month_Start_Date'])
    wei_data = pd.read_csv('wei_sample.csv')
    answer = pd.read_csv('dc_answer.csv')

    # set quantile cutoff to 0
    quant_cut = 0

    # create data structures for testing
    x_vals = list(answer['x_value'])
    fin = pd.DataFrame(columns={'x_value', 'domain_check'})

    # iterate over potential x values
    for i in range(0, len(x_vals)):
        # get x value for testing
        X = x_vals[i]
        fin.loc[i, 'x_value'] = X

        # test the x value
        df = domain_check(tmfh_data, wei_data, X, quant_cut, libraries)
        fin.loc[i, 'domain_check'] = df.iloc[0]['domain_check']

    # convert to match answer data types
    fin['x_value'] = fin['x_value'].astype('int64')

    # assert that the data frames are equal
    pd.testing.assert_frame_equal(fin, answer)


test(libraries)
