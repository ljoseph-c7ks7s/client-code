def domain_check(tm, wq, X, q_cut, libraries):
    """ Calculates window value columns to determine what periods a flight record could be grouped into.
    Example: '2016-01-04' would return window values '2015-11-01', '2015-12-01', '2016-01-01'.
    Args:
        tm: date frame from previous function
        wq: currently only works where period = 3. Long-term, will try and make dynamic based on this value
        X: quantile for domain check (note: converted to percentage)
        q_cut: quantile cut off for user to decide
        libraries: dictionary of libraries; access by name
    Returns:
       windowed: data frame with window values where record is active
    """
    pd = libraries['pandas']

    # initialize output data frame
    out = pd.DataFrame(index=[0], columns={'domain_check'})

    # compute fleet90_75 NOTE: this may require debug due to weird dict issue
    fleet90_75 = tm['Average_Flying_Hours'].quantile(X * .01)

    # keep only relevant columns from weibull quantiles
    wq = wq[['quantile', 'time']]

    # sort the data
    wq_sort = wq.sort_values(by=['quantile'], axis=0).reset_index(drop=True)

    # create an incremental time column & fill na's with time for missing (first) value
    wq_sort['incremental_time'] = wq_sort['time'] - wq_sort['time'].shift(periods=1)
    wq_sort['incremental_time'] = wq_sort['incremental_time'].fillna(wq_sort['time'])
    
    # cut off low end of quantile values
    try:
        # cut from quantile forward
        wq_fin = wq_sort.iloc[q_cut:]
    
        # compute min_inc_time
        min_inc_time = min(wq_fin['incremental_time'])
     
    except ValueError:
        print("Cutoff value out-of-bounds. Resetting to 0 for this test.")
        
        # cut from quantile forward
        wq_fin = wq_sort

        # compute min_inc_time
        min_inc_time = min(wq_fin['incremental_time'])

    # determine if it fails the domain check
    if min_inc_time > fleet90_75:
        out.iloc[0]['domain_check'] = 'Fail'
        print("{} percentile of flight hours accrued in 90 days, {}, is more than the minimum time change between 0.01 quantile increments, {}. Domain Check fails.".format(X, fleet90_75, min_inc_time))

    else:
        out.iloc[0]['domain_check'] = 'Pass'
        print("{} percentile of flight hours accrued in 90 days, {}, is less than the minimum time change between 0.01 quantile increments, {}. Domain Check passes.".format(X, fleet90_75, min_inc_time))

    return out


def fn(conn, libraries, params, predecessors):
    """
    Args:
        conn: connection to database for read access
        libraries: dictionary of libraries; access by name
        e.g. pd = libraries['pandas'] or stats = libraries['scipy']['stats']
        params: dictionary of additional parameters from component config (optional)
        predecessors: list of predecessor component names

    Returns:
        domain check results
    """
    pd = libraries["pandas"]

    # iterate through component list
    for pred in predecessors:
        if 'weibull' in pred:
            weibull_table_name = pred
        else:
            three_month_table_name = pred

    # load data from three month flight history collector
    query1 = "SELECT * FROM %s" % three_month_table_name
    three_month_flight_history = pd.read_sql(sql=query1, con=conn)

    # load data from single weibull quantities
    query2 = "SELECT * FROM %s WHERE type='tow_ci'" % weibull_table_name
    single_weibull_quantiles = pd.read_sql(sql=query2, con=conn)

    # grab parameter values
    X = params['X']  # default is 75
    quant_cut = params['Quantile_Cutoff']
    df_out = domain_check(three_month_flight_history, single_weibull_quantiles, X, quant_cut, libraries)

    return df_out
