"""Initial value definitions for UI filter components.

This module provides the function initialize_filters() which uses data to
determine the options and default values for UI filters in the application
layout.
"""


def initialize_filters(grad_rate_df):
    """Determine value options and defaults for UI filter components.

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

    # Extract values from data for districts, metrics, years, and subgroups
    districts = sorted(grad_rate_df['district'].dropna().unique())
    metrics = sorted(grad_rate_df['metric'].dropna().unique())
    years = sorted(grad_rate_df['year'].dropna().unique())
    subgroups = sorted(grad_rate_df['subgroup'].dropna().unique())

    # Set default values
    default_district = 'Canidae School District'
    default_metric = 'Four-Year Graduation Rate'

    # Use values to determine options and defaults for UI filter components
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
                for metric in metrics
            ],
            "value": default_metric if default_metric in metrics
            else metrics[0]
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
                for subgroup in subgroups
            ],
            "value": subgroups  # select all values by default
        }
    }

    return filter_configs
