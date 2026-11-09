import pandas as pd
from src.utils.disparity_calculations import get_disparity_df


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
