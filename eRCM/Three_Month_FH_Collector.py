"""

Args:
    conn: connection to database for read access
    libraries: dictionary of libraries; access by name
    e.g. pd = libraries['pandas'] or stats = libraries['scipy']['stats']
    params: dictionary of additional parameters from component config (optional)
    predecessors: list of predecessor component names

    Reads in compiled Sortie Data

Returns:
	average flight hours for the next three months
"""
def fn(conn, libraries, params, predecessors):
    pd = libraries['pandas']
    np = libraries['numpy']
    dt = libraries['datetime']

    last_date = str("20140101")

    query = "SELECT Serial_Number, Mission_Number, Depart_Date, Land_Date, Flying_Hours FROM %s WHERE Depart_Date >=" + last_date % predecessors[0]
    df = pd.read_sql_query(sql = query, con = conn)

    def CalcWindows(df, period):
        """ Calculates window value columns to determine what periods a flight record could be grouped into.
        Example: '2016-01-04' would return window values '2015-11-01', '2015-12-01', '2016-01-01'.
        Args:
            df: dateframe from previous function
            period: currently only works where period = 3. Long-term, will try and make dynamic based on this value
        Returns:
            windowed: dataframe with window values where record is active
        """
        # create useful window columns by iterating for 1 through number of periods specified
        for i in range(1, period + 1):
            #create column name and set window value (either 2, 1, or 0 when period = 3)
            column = 'W' + str(i)
            window = period - i

            # extract baseline month values
            df['Month'] = df['Depart_Date'].dt.month
            df['Year'] = df['Depart_Date'].dt.year

            # subset with loc to fix problematic time periods with year overlaps
            # if window is 2 and month is Jan or Feb, fix date accordingly
            if (window == 2):
                df.loc[(df.Month == 1) | (df.Month == 2), 'Year'] = df.Year - 1
                df.loc[(df.Month == 2), 'Month'] = 14
                df.loc[(df.Month == 1), 'Month'] = 13
            # if window is 1 and month is Jan, fix date accordingly
            elif (window == 1):
                df.loc[(df.Month == 1), 'Year'] = df.Year - 1
                df.loc[(df.Month == 1), 'Month'] = 13
            # else, use original month
            else:
                df['Month'] = df['Depart_Date'].dt.month

            # Decrement them month value based on the window value
            df['Month'] = df.Month - window

            # clean up date integer values by adding appropriate 0's and converting to strings
            df.loc[df.Month < 10, 'Month'] = '0' + df['Month'].astype(str) # add 0's to single digit months
            df.loc[df.Month >= 10, 'Month'] = df['Month'].astype(str) # do not add 0's to double digit months
            df['Year'] = df['Year'].astype(str)

            # create the value for each window as a string
            df[column] = df['Year'] + '-' + df['Month'] + '-01'
            # convert each window back to original datetime64 format
            df[column] = df[column].map(lambda x: np.datetime64(x))

            # drop the month and year columns
            windowed = df.drop(['Month', 'Year'], axis = 1)

        # return results
        return windowed


    def CalcRollingAvg(df, period):
        """ Calculates the rolling average by melting the window columns and grouping the result.
        Args:
         df: dateframe from previous function
         period: currently only works where period = 3. Long-term, will try and make dynamic based on this value
        Returns:
        grouped: dataframe with the moving average of flying_hours
        """
        # create a list of column values thus far
        columns = list(df.columns.values)

        # calculate the point at which the melted dataframe with pivot
        melt_axis = len(columns) - period

        # create a melted dataframe to used for group by calculation
        melted = pd.melt(df,
                         id_vars= columns[0:melt_axis],
                         value_vars = columns[melt_axis:8],
                         var_name = 'Window',
                         value_name = 'Window_Val'
                         )

        # group by window value and calculate the mean
        grouped = melted.groupby(['Window_Val'], as_index=False).mean()
        # rename columns
        grouped.rename(columns = {'Window_Val': 'Three_Month_Start_Date', 'Flying_Hours': 'Average_Flying_Hours'}, inplace = True)

        # return results
        return grouped


    def head(df, period=3):
        """ Calls the CalcWindows and CalcRollingAvg functions
        Args:
            df: dateframe from previous function
            period: currently only works where period = 3. Long-term, will try and make dynamic based on this value
        Returns:
            final: final dataframe
        """
        windows = CalcWindows(df, period)
        final = CalcRollingAvg(windows, period)

        return final


    # create the final dataframe
    final = head(df, period = 3)

    return final
