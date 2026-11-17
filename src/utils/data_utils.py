"""Utilities for processing data.

This module provides commonly-used utility functions for processing data sets
including calculations and transformations uing data.
"""

import pandas as pd


def get_disparity_df(grad_rate_df, metric, year):
    """Get data on graduation rate disparities in all districts.

    A district's graduation rate disparity is defined as the difference between
    its overall graduation rate and the lowest graduation rate across all
    demographic subgroups.

    Time complexity: O(N * M)

    Args:
        grad_rate_df (DataFrame): data set for graduation rates
        metric (string): metric used to determine graduation rates
        year (int): year of focus for analysis

    Returns:
        DataFrame: transformed data set with graduation rate disparity data,
            containing a column 'disparity' with the calculated disparity
            value for each school district
    """
    # Filter data
    # Filtering a DataFrame has time complexity O(N * M) with N rows and M
    # columns; in this context, M is constant
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
    # Given that both DataFrames have the same number of rows and this is
    # an inner join with a one-to-one key relationship, this join is O(N)
    district_disparity_df = pd.merge(
        baseline_df, min_subgroups_df, on='district', how='inner')

    # Add column for disparity; vectorized calculation is O(1)
    district_disparity_df['disparity'] = \
        district_disparity_df['baseline_all_students'] - \
        district_disparity_df['min_subgroup_grad_rate']

    return district_disparity_df


def get_gaps_df(grad_rate_df, metric, year):
    """Get data on graduation rate gaps for all subgroups.

    A graduation rate gap is defined as the difference between a subgroup's
    graduation rate and the overall graduation rate.

    This function assumes the input data set grad_rate_df has been filtered
    to include data for only one school district.

    Time complexity: O(N * M)

    Args:
        grad_rate_df (DataFrame): data set for graduation rates
        metric (string): metric used to measure graduation rates
        year (int): year of focus for analysis

    Returns:
        DataFrame: transformed data set with gaps data, containing a column
            'gap' with the value of the graduation rate gap for each
            subgroup
    """
    # Filter data
    # Filtering a DataFrame has time complexity O(N * M) with N rows and M
    # columns; in this context, M is constant
    grad_rate_filtered_df = grad_rate_df[
        (grad_rate_df['metric'] == metric) &
        (grad_rate_df['year'] == year)]

    # Extract baseline for comparison, grad rate for 'All Students'
    # Requires filtering which is O(N * M)
    baseline = grad_rate_filtered_df[
        grad_rate_filtered_df['subgroup'] == 'All Students']['value'].values[0]

    # Filter to exclude subgroup 'All Students'
    subgroups_gap_df = grad_rate_filtered_df[
        grad_rate_filtered_df['subgroup'] != 'All Students']

    # Add column for gap; vectorized calculation is O(1)
    subgroups_gap_df['gap'] = subgroups_gap_df['value'] - baseline

    return subgroups_gap_df
