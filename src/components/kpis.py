import pandas as pd
import src.utils.data_utils as data_utils


def get_statewide_grad_rate(grad_rate_df, metric, year):
    grad_rate_df_filtered = grad_rate_df[(grad_rate_df['district'] ==
                                          'Statewide School District') &
                                         (grad_rate_df['subgroup'] ==
                                          'All Students') &
                                         (grad_rate_df['year'] == year) &
                                         (grad_rate_df['metric'] == metric)]
    overall_grad_rate = grad_rate_df_filtered['value'].item()
    return overall_grad_rate


def get_median_grad_rate_disparity(grad_rate_df, metric, year, subgroups):
    # Filter by subgroups
    subgroups_to_include = subgroups + ['All Students']
    grad_rate_df_filtered = grad_rate_df[grad_rate_df['subgroup'].isin(
        subgroups_to_include)]

    district_disparity_df = data_utils.get_disparity_df(
        grad_rate_df_filtered, metric, year)

    # Determine district-level median disparity
    median_grad_rate_disparity = district_disparity_df['disparity'].median()
    return median_grad_rate_disparity


def get_pct_districts_improving_disparity(grad_rate_df, metric, start_year,
                                          stop_year, subgroups):
    # Filter by subgroups
    subgroups_to_include = subgroups + ['All Students']
    grad_rate_df_filtered = grad_rate_df[grad_rate_df['subgroup'].isin(
        subgroups_to_include)]

    disparity_start_year_df = data_utils.get_disparity_df(
        grad_rate_df_filtered, metric, start_year)[
        ['district', 'disparity']].rename(
            columns={'disparity': 'disparity_start'})

    disparity_stop_year_df = data_utils.get_disparity_df(
        grad_rate_df_filtered, metric, stop_year)[
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
    return pct_improving
