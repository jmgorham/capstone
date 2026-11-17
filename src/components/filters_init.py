"""Initial value definitions for UI filter components.

This module provides the function initialize_filters() which uses data to
determine the options and default values for UI filters in the application
layout.
"""

from src.utils.sorting_utils import sort_metrics, sort_subgroups


def initialize_filters(grad_rate_df):
    """Determine value options and defaults for UI filter components.

    Time complexity: O(N) for N rows of data

    Args:
        grad_rate_df (DataFrame): graduation rate data. Must include the
            following columns:
            - district
            - metric
            - year
            - subgroup

    Returns:
        dict: JSON-like structure containing initial settings for UI
            filter components.
            Example: {'districts': {'options': [1, 2], 'value': 1}}

    """
    # Filter out aggregates that should not be selectable
    # Filtering is O(N * M) for N rows and M columns
    grad_rate_df_filtered = grad_rate_df[(grad_rate_df['district']
                                          != 'Statewide School District') &
                                         (grad_rate_df['subgroup']
                                          != 'All Students')]

    # Extract values from data for districts, metrics, years, and subgroups
    # Each line is O(1) for extracting values from the DataFrame and
    # O(NlogN) for sorting each list, where N is the length of the list
    districts = sorted(grad_rate_df_filtered['district'].dropna().unique())
    metrics = sorted(grad_rate_df_filtered['metric'].dropna().unique())
    years = sorted(grad_rate_df_filtered['year'].dropna().unique())
    subgroups = sorted(grad_rate_df_filtered['subgroup'].dropna().unique())

    # Apply custom sorting orders to metrics and subgroups; O(NlogN)
    metrics_sorted = sort_metrics(metrics)
    subgroups_sorted = sort_subgroups(subgroups)

    # Set default values
    default_district = 'Canidae School District'
    default_metric = 'Four-Year Graduation Rate'

    # Use values to determine options and defaults for UI filter components
    # Full block is O(1)
    filter_configs = {

        # Defaults for school districts dropdown
        "districts": {
            "options": [  # list comprehension to build options based on data
                {"label": district, "value": district}
                for district in districts
            ],
            "value": default_district if default_district in districts
            else districts[0]
        },

        # Defaults for grad rate metric radio selector
        "metrics": {
            "options": [  # list comprehension to build options based on data
                {"label": metric, "value": metric}
                for metric in metrics_sorted
            ],
            "value": default_metric if default_metric in metrics_sorted
            else metrics_sorted[0]
        },

        # Defaults for year range selector
        "years": {
            "min": min(years),
            "max": max(years),
            "value": [min(years), max(years)]  # select full range by default
        },

        # Defaults for subgroup multi-selector checkboxes
        "subgroups": {
            "options": [  # list comprehension to build options based on data
                {"label": subgroup, "value": subgroup}
                for subgroup in subgroups_sorted
            ],
            "value": subgroups_sorted  # select all values by default
        }
    }

    return filter_configs
