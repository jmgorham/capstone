import pandas as pd


def get_disparity_df(grad_rate_df, metric, year):
    # Filter data
    grad_rate_filtered_df = grad_rate_df[(grad_rate_df['metric'] == metric) &
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
