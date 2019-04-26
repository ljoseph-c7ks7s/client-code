def limit_data_set(df, dselect, libraries):
    """ Limits the data set to only necessary columns and only relevant dates
    Args:
        df: date frame from previous function
        dselect: determines what will set the current date
        libraries: dictionary of libraries; access by name
        e.g. pd = libraries['pandas'] or stats = libraries['scipy']['stats']
    Returns:
        df: data frame with limited data
        ldate: last date for later time sub setting
    """
    dt = libraries['datetime']
    np = libraries['numpy']
    pd = libraries['pandas']

    # limit the data frame to desired columns
    df = df[['Serial_Number', 'Depart_Date', 'Flying_Hours']]

    # limit the data to the a certain time period
    if dselect == 'Today':
        ldate = dt.datetime.now().year - 5
    else:
        ldate = df['Depart_Date'].dt.year.max() - 5

    # limit the data frame to the correct time window
    df = df[df['Depart_Date'].dt.year >= ldate]

    # calculate the first of the month (replacing 0's if a single digit month)
    df['Fixed_Date'] = pd.to_datetime(df['Depart_Date']).apply(lambda x: '{year}-{month}-01'.format(year=x.year, month=x.month) if x.month > 9 else '{year}-0{month}-01'.format(year=x.year, month=x.month))
    df['Fixed_Date'] = df['Fixed_Date'].map(lambda x: np.datetime64(x))
    
    print('Limited Data COMPLETE')

    return df, ldate


def calc_monthly_values(df, libraries):
    """ Calculates the number of unique tail numbers present in each time window.
    Args:
        df: date frame from previous function
        libraries: dictionary of libraries; access by name
    Returns:
        totals: data frame with average flight hours
    """
    pd = libraries['pandas']

    # limit the data frame to desired columns
    df = df[['Serial_Number', 'Flying_Hours', 'Fixed_Date']]

    # group by month and calculate total flying hours and unique tails
    totals = df.groupby(['Fixed_Date'], as_index=False).agg(
        {'Serial_Number': pd.Series.nunique, 'Flying_Hours': pd.Series.sum})

    # calculate the monthly average
    totals['Monthly_Average'] = totals['Flying_Hours'] / totals['Serial_Number']

    # convert to data frame
    totals = pd.DataFrame(totals)

    # drop intermediate columns
    totals.drop(['Flying_Hours', 'Serial_Number'], axis=1, inplace=True)

    print('Monthly Values COMPLETE')

    return totals


def calc_windows(df, p, libraries):
    """ Calculates window value columns to determine what periods a flight record could be grouped into.
    Example: '2016-01-04' would return window values '2015-11-01', '2015-12-01', '2016-01-01'.
    Args:
        df: date frame from previous function
        p: currently only works where period = 3. Long-term, will try and make dynamic based on this value
        libraries: dictionary of libraries; access by name
        e.g. pd = libraries['pandas'] or stats = libraries['scipy']['stats']
    Returns:
        windowed: data frame with window values where record is active
    """
    np = libraries['numpy']

    # create useful window columns by iterating for 1 through number of periods specified
    for i in range(1, p + 1):
        # create column name and set window value (either 2, 1, or 0 when period = 3)
        column = 'W' + str(i)
        window = p - i

        # extract baseline month values
        df['Month'] = df['Fixed_Date'].dt.month
        df['Year'] = df['Fixed_Date'].dt.year

        # subset with loc to fix problematic time periods with year overlaps
        # if window is 2 and month is Jan or Feb, fix date accordingly
        if window == 2:
            df.loc[(df.Month == 1) | (df.Month == 2), 'Year'] = df.Year - 1
            df.loc[(df.Month == 2), 'Month'] = 14
            df.loc[(df.Month == 1), 'Month'] = 13
        # if window is 1 and month is Jan, fix date accordingly
        elif window == 1:
            df.loc[(df.Month == 1), 'Year'] = df.Year - 1
            df.loc[(df.Month == 1), 'Month'] = 13

        # Decrement them month value based on the window value
        df['Month'] = df.Month - window

        # clean up date integer values by adding appropriate 0's and converting to strings
        df.loc[df.Month < 10, 'Month'] = '0' + df['Month'].astype(str)  # add 0's to single digit months
        df.loc[df.Month >= 10, 'Month'] = df['Month'].astype(str)
        df['Year'] = df['Year'].astype(str)

        # create the value for each window as a string
        df[column] = df['Year'] + '-' + df['Month'] + '-01'

        # convert each window back to original datetime64 format
        df[column] = df[column].map(lambda x: np.datetime64(x))

    # drop the month and year columns
    windowed = df.drop(['Month', 'Year'], axis=1)

    print('Windows COMPLETE')

    return windowed


def calc_rolling_avg(df, last_date, p, libraries):
    """ Calculates the rolling average by melting the window columns and grouping the result.
    Args:
     df: date frame from previous function
     last_date: year associated with five years ago
     p: currently only works where period = 3. Long-term, will try and make dynamic based on this value
     libraries: dictionary of libraries; access by name
        e.g. pd = libraries['pandas'] or stats = libraries['scipy']['stats']
    Returns:
    grouped: data frame with the moving average of flying_hours
    """
    pd = libraries['pandas']

    # create a list of column values thus far
    columns = list(df.columns.values)

    # calculate the point at which the melted data frame with pivot
    melt_axis = len(columns) - p

    # create a melted data frame to used for group by calculation
    melted = pd.melt(df,
                     id_vars=columns[1:melt_axis],
                     value_vars=columns[melt_axis:len(columns)],
                     var_name='Window',
                     value_name='Window_Val'
                     )

    # group by window value and calculate the mean
    grouped = melted.groupby(['Window_Val'], as_index=False).sum()

    # rename columns
    grouped.rename(columns={'Window_Val': 'Three_Month_Start_Date', 'Monthly_Average': 'Average_Flying_Hours'}, inplace=True)

    # eliminate windows that predate the start year
    grouped = pd.DataFrame(grouped[grouped['Three_Month_Start_Date'].dt.year >= last_date])

    # eliminate the last two windows due to a lack of data
    grouped.drop(grouped.tail(2).index, inplace=True)

    print('Rolling Averages COMPLETE')

    return grouped


def fn(conn, libraries, params, predecessors):
    """
    Args:
        conn: connection to database for read access
        libraries: dictionary of libraries; access by name
        e.g. pd = libraries['pandas'] or stats = libraries['scipy']['stats']
        params: dictionary of additional parameters from component config (optional)
        predecessors: list of predecessor component names

        Reads in compiled sortie Data

    Returns:
        average flight hours for the next three months
    """
    pd = libraries['pandas']

    query = "SELECT * FROM %s" % predecessors[0]
    df = pd.read_sql_query(sql=query, con=conn)

    # set the period (will make this a parameter eventually)
    period = 3
    date_selection = 'Last_Record'

    # call the relevant functions
    ldf, last_date = limit_data_set(df, date_selection, libraries)
    tot = calc_monthly_values(ldf, libraries)
    win = calc_windows(tot, period, libraries)
    fin = calc_rolling_avg(win, last_date, period, libraries)

    return fin
