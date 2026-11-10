"""Utilities for sorting lists of data values.

This module provides functions for applying custom sorting orders to lists
of values, helping ensure that values are ordered meaningfully and
consistently."""


def sort_metrics(metrics):
    """Apply custom sorting to a list of metrics.

    Args:
        metrics (list<string>): metric values to sort

    Returns:
        list<string>: input list with custom sorting order applied
    """
    # Define desired custom sorting order for metrics
    default_metrics_sorting = ['Four-Year Graduation Rate',
                               'Five-Year Graduation Rate',
                               'Six-Year Graduation Rate']

    # Function to map each item to its index in default_metrics_sorting
    def sort_key(x): return default_metrics_sorting.index(x) \
        if x in default_metrics_sorting else len(default_metrics_sorting)

    # Sort input list according to sort_key
    metrics_sorted = sorted(metrics, key=sort_key)

    return metrics_sorted


def sort_subgroups(subgroups):
    """Apply custom sorting to a list of subgroups.

    Args:
        subgroups (list<string>): subgroup values to sort

    Returns:
        list<string>: input list with custom sorting order applied
    """
    # Define custom sorting order for subgroups
    default_subgroups_sorting = [
        'All Students', 'Female', 'Male', 'Non-binary',
        'American Indian or Alaska Native',
        'Asian or Native Hawaiian/Other Pacific Islander',
        'Black or African American', 'Hispanic or Latino', 'White',
        'Multiracial', 'Economically Disadvantaged',
        'English Language Learner', 'Homeless', 'In Foster Care', 'Migrant',
        'Parent in Armed Forces', 'Students with Disabilities'
    ]

    # Function to map each item to its index in default_subgroups_sorting
    def sort_key(x): return default_subgroups_sorting.index(x) \
        if x in default_subgroups_sorting else len(default_subgroups_sorting)

    # Sort input list according to sort_key
    subgroups_sorted = sorted(subgroups, key=sort_key)

    return subgroups_sorted
