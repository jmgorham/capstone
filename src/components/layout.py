"""App component for defining UI layout.

This module provides the function create_layout() for defining and returning
the application's UI layout, including all UI components required for the app's
interactive functionality.
"""

import dash_bootstrap_components as dbc
from dash import dcc, html


def create_layout():
    """Define the app's frontend UI layout.

    Returns:
        dbc.Container: UI layout for Dash app, including all
            components required for interactive functionality.
    """
    layout = dbc.Container([
        # Container object contains Row objects as children
        # Row objects contain Col objects as children

        # ROW 1: Dashboard title and header
        dbc.Row([
            dbc.Col(
                html.H1("TITLE",
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
                                    options=[
                                        {'label': 'Option 1', 'value': '1'},
                                        {'label': 'Option 2', 'value': '2'},
                                        {'label': 'Option 3', 'value': '3'}
                                    ],
                                    value='1',  # default selection
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
                                    options=[
                                        {'label': 'Metric 1', 'value': '1'},
                                        {'label': 'Metric 2', 'value': '2'},
                                        {'label': 'Metric 3', 'value': '3'}
                                    ],
                                    value='1',  # default selection
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
                                    min=2020,
                                    max=2025,
                                    # Enforce 1-year step intervals
                                    step=1,
                                    # Dict comprehension to place marks
                                    # on the range selector element
                                    # at every year between min and max
                                    marks={year: str(year)
                                           for year in range(2020, 2026)},
                                    value=[2021, 2023]  # default range
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
                                    options=[
                                        {'label': 'Subgroup 1', 'value': '1'},
                                        {'label': 'Subgroup 2', 'value': '2'},
                                        {'label': 'Subgroup 3', 'value': '3'}
                                    ],
                                    value=['1', '2', '3']  # default selections
                                )
                            ])

                        ], gap=3)  # gap provides vertical padding
                    ])
                ], color="light")  # color for background of card container
            ], width=3),  # sidebar fills 3 columns, or 1/4 of screen width

            # COL 2: Main content for core dashboard visualizations
            dbc.Col([

                # ROW 1: 3 KPI tiles
                dbc.Row([

                    # KPI 1: Overall grad rate
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                # KPI title
                                html.H6("KPI Tile 1"),
                                # KPI value, handled by callbacks
                                html.H2("50.00%",  # placeholder value
                                        id="kpi-grad-rate")
                            ])
                        ])
                    ]),

                    # KPI 2: Median disparity
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                # KPI title
                                html.H6("KPI Tile 2"),
                                # KPI value, handled by callbacks
                                html.H2("12pp",  # placeholder value
                                        id="kpi-disparity")
                            ])
                        ])
                    ]),

                    # KPI 3: Pct improving
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                # KPI title
                                html.H6("KPI Tile 3"),
                                # KPI value, handled by callbacks
                                html.H2("65%",  # placeholder value
                                        id="kpi-pct-improving")

                            ])
                        ])
                    ]),

                ], className="mb-4"),  # add vertical padding

                # ROW 2: Info on selected school district
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                # Text content handled by callbacks
                                html.H6("Info on Selected District",
                                        id="district-info-text")
                            ])
                        ])
                    ])
                ], className="mb-4"),  # add vertical padding

                # ROW 3: 2 data visualizations
                dbc.Row([

                    # VIZ 1: Line chart of grad rate over time
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("Data Visualization 1")
                            ])
                        ])
                    ]),

                    # VIZ 2: Dumbbell chart of gaps over time
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("Data Visualization 2")
                            ])
                        ])
                    ])
                ], className="mb-4"),  # add vertical padding

                # ROW 4: 1 data visualization
                dbc.Row([

                    # VIZ 3: Network adjacency graph of districts
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("Data Visualization 3")
                            ])
                        ])
                    ])
                ])

            ], width=9)  # main body takes up 9 columns or 3/4 of screen

        ])
    ], fluid=True)  # container stretches to fill entire width of screen

    return layout
