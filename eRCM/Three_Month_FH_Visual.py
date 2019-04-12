def fn(conn, libraries, params, predecessors):
    """
    Plot bar chart with categorical x axis

    Args: 
        conn: connection to database for read access
        libraries: dictionary of libraries; access by name,
            e.g. pd = libraries['pd'] or stats = libraries['scipy']['stats']        
        params: dictionary of additional parameters from component config
        predecessors: list of predecessor component names
            names are lower-case with underscores instead of spaces
            to match database tables

    Returns:
        None

    Side Effects:
    """
     
    # library 'imports'
    np = libraries["numpy"]
    pd = libraries["pandas"]
    plotting = libraries["bokeh"]["plotting"]
    io = libraries["bokeh"]["io"]
    models = libraries["bokeh"]["models"]
    layouts = libraries["bokeh"]["layouts"]

    # load data
    query = "SELECT * FROM %s" % predecessors[0]
    df = pd.read_sql(sql = query, con = conn)

    # generate axis labels
    cnames = list(df.columns.values)
    xlabel = cnames[0].replace("_", " ")
    ylabel = cnames[1].replace("_", " ")

    # create initial plot
    plot = plotting.figure(title = 'Average Flight Hours for Three Month Rolling Window',
                           x_axis_type="datetime", 
                           x_axis_label = xlabel,
                           y_axis_label = ylabel,
                           width=1200)

    # create initial plot
    plot = plotting.figure(title = 'Average Flight Hours for Three Month Rolling Window',
                           x_axis_type="datetime", 
                           x_axis_label = xlabel,
                           y_axis_label = ylabel,
                           width=1000)
    
    # add trend line
    plot.line(x = df[cnames[0]],
              y = df[cnames[1]])
    
    # format the x-axis tick labels
    plot.xaxis.formatter = models.DatetimeTickFormatter(
            hours=["%Y-%m"],
            days=["%Y-%m"],
            months=["%Y-%m"],
            years=["%Y-%m"],
        )

    # save the plot
    io.save(plot)

    return

