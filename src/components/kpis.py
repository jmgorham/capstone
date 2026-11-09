import pandas as pd


def get_statewide_grad_rate(grad_rate_df):
    grad_rate_df_filtered = grad_rate_df[(grad_rate_df['district'] ==
                                          'Statewide School District') &
                                         (grad_rate_df['subgroup'] ==
                                          'All Students') &
                                         (grad_rate_df['year'] == 2025) &
                                         (grad_rate_df['metric']
                                          == 'Four-Year Graduation Rate')]
    overall_grad_rate = grad_rate_df_filtered['value'].item()
    overall_grad_rate = round(overall_grad_rate, 1)
    return overall_grad_rate


def get_median_grad_rate_disparity(grad_rate_df):
    district_disparity_df = get_disparity_df(grad_rate_df, 2025)

    # Determine district-level median disparity
    median_grad_rate_disparity = district_disparity_df['disparity'].median()
    median_grad_rate_disparity = round(median_grad_rate_disparity, 1)
    return median_grad_rate_disparity


def get_pct_districts_improving_disparity(grad_rate_df):
    disparity_start_year_df = get_disparity_df(grad_rate_df, 2020)[
        ['district', 'disparity']].rename(
            columns={'disparity': 'disparity_start'})

    disparity_stop_year_df = get_disparity_df(grad_rate_df, 2025)[
        ['district', 'disparity']].rename(
            columns={'disparity': 'disparity_stop'})

    # Join dataframes
    disparity_change_df = pd.merge(
        disparity_start_year_df, disparity_stop_year_df,
        on='district', how='inner')
    disparity_change_df['change'] = disparity_change_df['disparity_stop'] - \
        disparity_change_df['disparity_start']

    # Calculate percent improving
    pct_improving = (disparity_change_df['change'] < 0).mean() * 100
    pct_improving = round(pct_improving, 1)

    return pct_improving


def get_disparity_df(grad_rate_df, year):
    # Filter data
    grad_rate_filtered_df = grad_rate_df[(grad_rate_df['metric']
                                          == 'Four-Year Graduation Rate') &
                                         (grad_rate_df['year'] == year) &
                                         (grad_rate_df['district']
                                          != 'Statewide School District')]

    # Get a dataframe for baseline grad rates by district ('All Students')
    baseline_df = grad_rate_filtered_df[
        grad_rate_filtered_df['subgroup'] == 'All Students']
    baseline_df = baseline_df[['district', 'value']].rename(
        columns={'value': 'baseline_all_students'})

    # Get a dataframe with the min grad rate subgroup value for each district
    subgroups_df = grad_rate_filtered_df[
        grad_rate_filtered_df['subgroup'] != 'All Students']
    min_subgroups_df = subgroups_df.loc[subgroups_df.groupby('district')[
        'value'].idxmin()]
    min_subgroups_df = min_subgroups_df[['district', 'value']].rename(
        columns={'value': 'min_subgroup_grad_rate'})

    # Perform an inner join on the two dataframes
    district_disparity_df = pd.merge(
        baseline_df, min_subgroups_df, on='district', how='inner')

    # Add column for disparity
    district_disparity_df['disparity'] = \
        district_disparity_df['baseline_all_students'] - \
        district_disparity_df['min_subgroup_grad_rate']

    return district_disparity_df
