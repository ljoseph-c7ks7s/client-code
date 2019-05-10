def sort_rules(df, libraries):
    pd = libraries['pandas']
    re = libraries['re']

    # regex for finding all contain/contains that are not proceeded by 'not', OR anything that does not contain 'contain'
    pattern = r'^.*(?<!not )contains.*$|^.*(?<!not )contain.*$|^(?!.*contain).*^'

    # create flag based on regex and sort by contains_flag then rule_number
    df['contains_flag'] = df.rule.apply(lambda x: 0 if re.search(pattern, x, re.IGNORECASE) else 1)

    # remove all letters before int conversion
    df.rule_number = df.rule_number.str.extract(r'(\d+)', expand=False).astype(int)

    df.sort_values(by=['contains_flag', 'rule_number'], ascending=True, inplace=True)

    # set the sort order according to AF spec
    level_order = ['Level 3', 'Level 3 High', 'Level 3 High Promoted', 'Level 3 High Double Promoted', 'Level 3 Low',
                   'Level 3 Low Promoted', 'Level 3 Low Double Promoted', 'Level 3 4F4', 'Level 3 4F5', 'Level 3 5F5'
                                                                                                        'Level 4', 'Level 4 High', 'Level 4 High Promoted', 'Level 4 Low', 'Level 4 Low Promoted',
                   'Level 4 5F5', 'Level 5', 'Level 5 High', 'Level 5 Low']

    # create subset dfs and concat at the end
    df_sort_list = []

    for level in level_order:
        df_sort_list.append(df[df.level == level])

    df_sorted = pd.concat(df_sort_list)

    # drop the contains_flag
    df_sorted.drop(['rule_number', 'contains_flag'], axis=1, inplace=True)

    return df_sorted
    

def fn(conn, libraries, params, predecessors):

    pd = libraries['pandas']

    query = """SELECT level, rule_number, rule FROM {} WHERE type = 'Edit'""".format(predecessors[0])
    df = pd.read_sql(sql=query, con=conn)

    df_sort = sort_rules(df, libraries)

    return df_sort
