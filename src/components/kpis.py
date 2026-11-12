"""App component for defining KPI calculations.

This module contains functions for calculating KPIs displayed on the app
dashboard including filtering by school district, graduation rate metric,
years of focus, and demographic subgroups of focus.
"""


import pandas as pd

from src.utils import data_utils


def get_statewide_grad_rate(grad_rate_df, metric, year):
    """Calculate the statewide baseline graduation rate.

    This metric is not impacted by selections of district or subgroup. It is
    a state-level aggregate and uses the subgroup 'All Students' as a baseline
    value.

    Args:
        grad_rate_df (DataFrame): data set for graudation rates
        metric (string): metric used to measure graduation rates
        year (int): year of focus for graduation rate analysis

    Returns:
        string: overall statewide graduation rate, formatted for visualization
    """
    # Filter data
    grad_rate_df_filtered = grad_rate_df[
        # Extract statewide aggregate values
        (grad_rate_df['district'] == 'Statewide School District') &
        # Extract aggregate of all demographic subgroups
        (grad_rate_df['subgroup'] == 'All Students') &
        (grad_rate_df['year'] == year) &
        (grad_rate_df['metric'] == metric)]

    # Extract overall graduation rate from filtered data
    overall_grad_rate = grad_rate_df_filtered['value'].item()

    # Format for visualization
    overall_grad_rate_kpi_string = f'{overall_grad_rate:.1f}%'

    return overall_grad_rate_kpi_string


def get_median_grad_rate_disparity(grad_rate_df, metric, year, subgroups):
    """Calculate the district-level median of graduation rate disparities.

    This metric is not impacted by selections of district. It is a state-level 
    aggregate.

    Args:
        grad_rate_df (DataFrame): data set for graudation rates
        metric (string): metric used to measure graduation rates
        year (int): year of focus for graduation rate analysis
        subgroups (list<string>): demographic subgroups of focus for analysis

    Returns:
        string: overall statewide graduation rate, formatted for visualization
    """
    # Filter by subgroups, including 'All Students' as a baseline
    subgroups_to_include = subgroups + ['All Students']
    grad_rate_df_filtered = grad_rate_df[grad_rate_df['subgroup'].isin(
        subgroups_to_include)]

    # Calculate graduation rate disparities for all districts
    district_disparity_df = data_utils.get_disparity_df(
        grad_rate_df_filtered, metric, year)

    # Determine district-level median disparity
    median_grad_rate_disparity = district_disparity_df['disparity'].median()

    # Format for visualization
    median_grad_rate_disparity_kpi_string = \
        f'{median_grad_rate_disparity:.1f}pp'

    return median_grad_rate_disparity_kpi_string


def get_pct_districts_improving_disparity(grad_rate_df, metric, start_year,
                                          stop_year, subgroups):
    """Calculate the percentage of districts reducing grad rate disparities.

    This metric is not impacted by selections of district. It is a state-level
    aggregate.

    Args:
        grad_rate_df (DataFrame): data set for graudation rates
        metric (string): metric used to measure graduation rates
        start_year (int): minimum year of focus for graduation rate analysis
        stop_year (int): maximum year of focus for graduation rate analysis
        subgroups (list<string>): demographic subgroups of focus for analysis

    Returns:
        string: percentage of school districts improving disparities,
            formatted for visualization
    """
    # Filter by subgroups, including 'All Students' as a baseline
    subgroups_to_include = subgroups + ['All Students']
    grad_rate_df_filtered = grad_rate_df[grad_rate_df['subgroup'].isin(
        subgroups_to_include)]

    # Calculate graduation rate disparities for start_year
    disparity_start_year_df = data_utils.get_disparity_df(
        grad_rate_df_filtered, metric, start_year)[
        ['district', 'disparity']].rename(
            columns={'disparity': 'disparity_start'})

    # Calculate graduation rate disparities for stop_year
    disparity_stop_year_df = data_utils.get_disparity_df(
        grad_rate_df_filtered, metric, stop_year)[
        ['district', 'disparity']].rename(
            columns={'disparity': 'disparity_stop'})

    # Join dataframes to determine changes in disparities for all districts
    disparity_change_df = pd.merge(
        disparity_start_year_df, disparity_stop_year_df,
        on='district', how='inner')

    # Add column for change in disparity
    disparity_change_df['change'] = disparity_change_df['disparity_stop'] - \
        disparity_change_df['disparity_start']

    # Calculate percent improving
    # Negative change indicates a disparity that is lower at the end of the
    # time interval, and is therefore improving
    pct_improving = (disparity_change_df['change'] < 0).mean() * 100

    # Format for visualization
    pct_improving_kpi_string = f'{pct_improving:.1f}%'

    return pct_improving_kpi_string
