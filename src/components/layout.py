"""App component for defining UI layout.

This module provides the function create_layout() for defining and returning
the application's UI layout, including all UI components required for the app's
interactive functionality.
"""

import dash_bootstrap_components as dbc
from dash import dcc, html

import src.components.visualizations as viz
import src.components.kpis as kpis
from src.components.filters_init import initialize_filters


def create_layout(grad_rate_df):
    """Define the app's frontend UI layout.

    Args:
        grad_rate_df (DataFrame): graduation rates data. Must contain the
            following columns:
            - district
            - metric
            - year
            - subgroup
            - value

    Returns:
        dbc.Container: UI layout for Dash app, including all
            components required for interactive functionality.
    """
    # Use data to get default config values for UI filter components
    # JSON-like dictionary data with default settings
    filter_defaults = initialize_filters(grad_rate_df)

    # Build dashboard layout
    layout = dbc.Container([
        # Container object contains Row objects as children
        # Row objects contain Col objects as children

        # ROW 1: Dashboard title and header
        dbc.Row([
            dbc.Col(
                html.H1("Equity in Education Dashboard: Graduation Rates "
                        "in New York State School Districts",
                        # className argument gives style info
                        className="text-center my-4 text-primary"),
                # Bootstrap Components divides screens into 12 columns
                # width=12 dictates width should span full screen
                width=12
            )
        ]),

        # ROW 2: Main content area
        dbc.Row([

            # COL 1: Sidebar for UI filters and interactive elements
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        # Stack container helps with vertical padding
                        dbc.Stack([

                            # COMPONENT 1: UI dropdown search bar
                            # for selecting a district
                            html.Div([
                                # Explanatory label for UI element
                                html.Label("School district:"),

                                # Dropdown selector for school district
                                dcc.Dropdown(
                                    # ID tag used for callbacks
                                    id="district-select-dropdown",
                                    options=filter_defaults['districts']
                                    ['options'],
                                    # Value determines default selection
                                    value=filter_defaults['districts']
                                    ['value'],
                                    searchable=True,  # adds search bar
                                    clearable=True,  # adds 'X' to clear
                                    # Placeholder creates text hint for search
                                    placeholder='Type to search...',
                                )
                            ]),

                            # COMPONENT 2: UI radio buttons for
                            # selecting a metric for analysis
                            html.Div([
                                # Explanatory label for UI element
                                html.Label("Graduation rate metric:"),

                                # RadioItems: buttons where users select
                                # exactly 1 option
                                dcc.RadioItems(
                                    # ID tag used for callbacks
                                    id="metric-select-radio",
                                    options=filter_defaults['metrics']
                                    ['options'],
                                    # Value determines default selection
                                    value=filter_defaults['metrics']['value'],
                                    inline=False  # stack vertically
                                )
                            ]),

                            # COMPONENT 3: UI date range selector
                            html.Div([
                                # Explanatory label for UI element
                                html.Label("Time period:"),

                                # RangeSlider is used instead of
                                # DateRangePicker because DateRangePicker
                                # uses full dates and does not support
                                # using just years.
                                dcc.RangeSlider(
                                    # ID tag used for callbacks
                                    id='year-range-select',
                                    # Min and max allowable years
                                    min=filter_defaults['years']['min'],
                                    max=filter_defaults['years']['max'],
                                    # Enforce 1-year step intervals
                                    step=1,
                                    # Dict comprehension to place marks
                                    # on the range selector element
                                    # at every year between min and max
                                    marks={year: str(year)
                                           for year in range(2020, 2026)},
                                    # Value determines default selection
                                    value=filter_defaults['years']['value']
                                )
                            ]),

                            # COMPONENT 4: UI buttons for subgroups to include
                            html.Div([
                                # Explanatory label for UI element
                                html.Label('Subgroups included in analysis:'),

                                # Checklist to select any number of options
                                dcc.Checklist(
                                    # ID tag used for callbacks
                                    id='subgroup-select-checklist',
                                    options=filter_defaults['subgroups']
                                    ['options'],
                                    # Value determines default selection
                                    value=filter_defaults['subgroups']['value']
                                )
                            ])

                        ], gap=4)  # gap provides vertical padding
                    ])
                ],
                    color="light",  # color for background of card container
                    # Force card to fill full horizontal and vertical space
                    className="h-100 w-100"
                )
            ],
                width=3,  # sidebar fills 3 columns, or 1/4 of screen width'
                # Stretch column container vertically as a flex container
                className="d-flex mb-4"
            ),

            # COL 2: Main content for core dashboard visualizations
            dbc.Col([

                # ROW 1: 3 KPI tiles
                dbc.Row([

                    # KPI 1: Overall grad rate
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                # KPI title
                                html.H6("Statewide Graduation Rate"),
                                # KPI value, handled by callbacks
                                html.H2('',  # placeholder dummy value
                                        id="kpi-grad-rate")
                            ])
                        ])
                    ]),

                    # KPI 2: Median disparity
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                # KPI title
                                html.H6("Median Graduation Rate Disparity"),
                                # KPI value, handled by callbacks
                                html.H2('',  # placeholder dummy value
                                        id="kpi-disparity")
                            ])
                        ])
                    ]),

                    # KPI 3: Pct improving
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                # KPI title
                                html.H6("Districts Improving Disparity"),
                                # KPI value, handled by callbacks
                                html.H2('',  # placeholder dummy value
                                        id="kpi-pct-improving")

                            ])
                        ])
                    ]),

                ], className="mb-4"),  # add vertical padding

                # ROW 2: 2 data visualizations
                dbc.Row([

                    # VIZ 1: Line chart of grad rate over time
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("Data Visualization 1"),
                                dcc.Graph(
                                    # Graph ID for callbacks
                                    id='grad-rate-line-chart',
                                    figure=viz.get_init_line_chart(
                                        grad_rate_df)
                                )
                            ])
                            # Force card to fill ful available space
                        ], className="h-100 w-100")
                    ], width=6,  # width should span half of container
                        className="d-flex"),

                    # VIZ 2: Dumbbell chart of gaps over time
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("Data Visualization 2"),
                                dcc.Graph(
                                    # Graph ID for callbacks
                                    id='gaps-dumbbell-chart',
                                    figure=viz.get_init_dumbbell_chart(
                                        grad_rate_df)
                                )
                            ])
                            # Force card to fill full available space
                        ], className="h-100 w-100")
                    ], width=6,  # width should span half of container
                        className="d-flex")
                    # Add vertical padding, force columns to stay same height
                ], className="mb-4 flex-grow-1 align-items-streth"),

                # ROW 3: 1 data visualization
                dbc.Row([

                    # VIZ 3: Network adjacency graph of districts
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("Data Visualization 3"),
                                dcc.Graph(
                                    # Graph ID for callbacks
                                    id='district-network-graph-chart',
                                    figure=viz.get_init_network_chart_dummy(
                                        grad_rate_df)
                                )
                            ])
                        ])
                    ])
                ])

            ],
                width=9,  # main body takes up 9 columns or 3/4 of screen
                className="mb-4"  # add vertical padding at bottom
            )

        ],
            # Keep both columsn the same height
            # Change overall height based on Container constraints
            className="flex-grow-1 align-items-stretch"
        )
    ],
        fluid=True  # container stretches to fill entire width of screen]
    )

    return layout
