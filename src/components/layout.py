"""App component for defining UI layout.

This module provides the function create_layout() for defining and returning
the application's UI layout, including all UI components required for the app's
interactive functionality.
"""

import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_iconify import DashIconify

import src.components.kpis as kpis
import src.components.visualizations as viz
from src.components.filters_init import initialize_filters


def create_layout(grad_rate_df, district_df):
    """Define the app's frontend UI layout.

    Args:
        grad_rate_df (DataFrame): data set for graduation rates
        district_df (DataFrame): data set for school districts

    Returns:
        dbc.Container: UI layout for Dash app, including all
            components required for interactive functionality
    """
    # Use data to get default config values for UI filter components
    # JSON-like dictionary data with default settings
    filter_defaults = initialize_filters(grad_rate_df)

    # Use defaults to calculate KPIs

    kpi_statewide_grad_rate = kpis.get_statewide_grad_rate(
        grad_rate_df,
        filter_defaults['metrics']['value'],
        filter_defaults['years']['value'][1]
    )

    kpi_median_disparity = kpis.get_median_grad_rate_disparity(
        grad_rate_df,
        filter_defaults['metrics']['value'],
        filter_defaults['years']['value'][1],
        filter_defaults['subgroups']['value']
    )

    kpi_pct_improving = kpis.get_pct_districts_improving_disparity(
        grad_rate_df,
        filter_defaults['metrics']['value'],
        filter_defaults['years']['value'][0],
        filter_defaults['years']['value'][1],
        filter_defaults['subgroups']['value']
    )

    # Format default titles for KPIs
    kpi_statewide_grad_rate_title = kpis.get_statewide_grad_rate_kpi_title(
        filter_defaults['years']['value'][1]
    )

    kpi_median_disparity_title = kpis.get_median_grad_rate_disparity_kpi_title(
        filter_defaults['years']['value'][1]
    )

    kpi_pct_improving_title = kpis.get_pct_improving_kpi_title(
        filter_defaults['years']['value'][0],
        filter_defaults['years']['value'][1]
    )

    # Use defaults to create initial visualizations

    viz_line_chart = viz.get_grad_rate_line_chart(
        grad_rate_df,
        filter_defaults['districts']['value'],
        filter_defaults['metrics']['value'],
        filter_defaults['years']['value'][0],
        filter_defaults['years']['value'][1],
        filter_defaults['subgroups']['value']
    )

    viz_dumbbell_chart = viz.get_disparity_dumbbell_chart(
        grad_rate_df,
        filter_defaults['districts']['value'],
        filter_defaults['metrics']['value'],
        filter_defaults['years']['value'][0],
        filter_defaults['years']['value'][1],
        filter_defaults['subgroups']['value']
    )

    viz_network_chart = viz.get_districts_network_chart(
        district_df,
        grad_rate_df,
        filter_defaults['districts']['value'],
        filter_defaults['metrics']['value'],
        filter_defaults['years']['value'][0],
        filter_defaults['years']['value'][1],
        filter_defaults['subgroups']['value']
    )

    # Format default chart titles
    viz_line_chart_title = viz.get_line_chart_title(
        filter_defaults['districts']['value']
    )

    viz_dumbbell_chart_title = viz.get_dumbbell_chart_title(
        filter_defaults['districts']['value']
    )

    viz_network_chart_title = viz.get_network_chart_title(
        filter_defaults['years']['value'][1]
    )

    # Build dashboard layout
    layout = dbc.Container([
        # Container object contains Row objects as children
        # Row objects contain Col objects as children

        # ROW: Main content area
        dbc.Row([

            # COL 1: Sidebar for UI filters and interactive elements
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        # Stack container helps with vertical padding
                        dbc.Stack([

                            # Sidebar header
                            html.Div([
                                html.H4(
                                    children=[
                                        DashIconify(icon='material-symbols'
                                                    ':data-exploration'
                                                    '-outline-sharp',
                                                    color='#593980'),
                                        " Equity in Education"
                                    ],
                                    className='d-flex align-items-center '
                                    'gap-2 custom-title text-wrap text-break',
                                    style={"overflowWrap": "break-word",
                                           "wordWrap": "break-word"}
                                ),
                                html.Div('An exploratoy analytics dashboard',
                                         className='custom-subtitle')
                            ]),

                            html.Hr(),

                            # COMPONENT 1: UI dropdown search bar
                            # for selecting a district
                            html.Div([
                                # Explanatory label for UI element
                                html.Label("School district:",
                                           className='custom-title'),

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
                                    placeholder='Type to search...'
                                )
                            ]),

                            html.Hr(),

                            # COMPONENT 2: UI radio buttons for
                            # selecting a metric for analysis
                            html.Div([
                                # Explanatory label for UI element
                                html.Label("Metric:",
                                           className='custom-title'),

                                # RadioItems: buttons where users select
                                # exactly 1 option
                                dcc.RadioItems(
                                    # ID tag used for callbacks
                                    id="metric-select-radio",
                                    options=filter_defaults['metrics']
                                    ['options'],
                                    # Value determines default selection
                                    value=filter_defaults['metrics']['value'],
                                    inline=False,  # stack vertically
                                    labelStyle={'overflowWrap': 'break-word',
                                                'wordBreak': 'break-word'}
                                )
                            ]),

                            html.Hr(),

                            # COMPONENT 3: UI date range selector
                            html.Div([
                                # Explanatory label for UI element
                                html.Label("Years:",
                                           className='custom-title'),

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
                                    value=filter_defaults['years']['value'],
                                    allowCross=False,
                                    allow_direct_input=False,
                                    pushable=1  # ensure years are not the same
                                )
                            ]),

                            html.Hr(),

                            # COMPONENT 4: UI buttons for subgroups to include
                            html.Div([
                                # Explanatory label for UI element
                                html.Label('Subgroups:',
                                           className='custom-title'),

                                # Checklist to select any number of options
                                dcc.Checklist(
                                    # ID tag used for callbacks
                                    id='subgroup-select-checklist',
                                    options=filter_defaults['subgroups']
                                    ['options'],
                                    # Value determines default selection
                                    value=filter_defaults['subgroups']
                                    ['value'],
                                    labelStyle={'overflowWrap': 'break-word',
                                                'wordBreak': 'break-word'}
                                )
                            ])
                        ], gap=3)  # gap provides vertical padding
                    ]),

                    # FOOTER
                    html.Footer(
                        children=[
                            html.H6('Developed by Jenna Gorham, Data Analyst'),

                            # Stack container to pair icon and text
                            html.A([
                                dbc.Stack([
                                    DashIconify(icon='mdi:linkedin', width=16),
                                    html.Span('LinkedIn')
                                ], direction='horizontal',
                                    gap=2,
                                    className='align-items-center text-wrap '
                                    'text-break',
                                    style={'overflowWrap': 'break-word',
                                           'wordWrap': 'break-word'}
                                )
                            ],
                                href='https://www.linkedin.com/in/jmgorham/',
                                target='_blank',
                                style={"color": "inherit",
                                       "textDecoration": "none"}
                            ),

                            # Stack container to pair icon and text
                            html.A([
                                dbc.Stack([
                                    DashIconify(icon='mdi:github', width=16),
                                    html.Span('GitHub')
                                ], direction='horizontal',
                                    gap=2,
                                    className='align-items-center text-wrap '
                                    'text-break',
                                    style={'overflowWrap': 'break-word',
                                           'wordWrap': 'break-word'}
                                )
                            ],
                                href='https://github.com/jmgorham',
                                target='_blank',
                                style={"color": "inherit",
                                       "textDecoration": "none"}
                            ),

                            # Stack container to pair icon and text
                            html.A([
                                dbc.Stack([
                                    DashIconify(
                                        icon='mdi:account-circle-outline',
                                        width=16),
                                    html.Span('Analytics Portfolio')
                                ], direction='horizontal',
                                    gap=2,
                                    className='align-items-center text-wrap '
                                    'text-break',
                                    style={'overflowWrap': 'break-word',
                                           'wordWrap': 'break-word'}
                                )
                            ],
                                href='https://jmgorham.github.io/portfolio/',
                                target='_blank',
                                style={"color": "inherit",
                                       "textDecoration": "none"}
                            ),

                            html.Br(),

                            # Link to data source
                            html.Span(
                                'Data from the New York State '
                                'Education Department: '),
                            html.A('data.nysed.gov',
                                   href='https://data.nysed.gov/',
                                   target='_blank',
                                   style={"color": "inherit"})

                        ],
                        className='mt-auto pt-3 border-top text-muted '
                        'card-footer'
                    )

                ],
                    # Force card to fill full horizontal and vertical space
                    className="h-100 w-100 custom-sidebar-card"
                )
            ],
                width=2,  # sidebar fills 2 columns, or 1/6 of screen width'
                # Stretch column container vertically as a flex container
                className="d-flex"
            ),

            # COL 2: Main content for core dashboard visualizations
            dbc.Col([

                # ROW 0: Dashboard title and header
                dbc.Row([
                    dbc.Col(
                        html.H1("Graduation Rate Equity "
                                "in New York State School Districts",
                                # className argument gives style info
                                className="text-center my-4 custom-title"),
                        # Bootstrap Components divides screens into 12 columns
                        # width=12 dictates width should span full screen
                        width=12
                    )
                ]),

                # ROW 1: 3 KPI tiles
                dbc.Row([

                    # KPI 1: Overall grad rate
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                # KPI title
                                html.H5(kpi_statewide_grad_rate_title,
                                        className='custom-title',
                                        id='kpi-grad-rate-title'),
                                # KPI value, handled by callbacks
                                html.H2(kpi_statewide_grad_rate,
                                        id="kpi-grad-rate",
                                        className='custom-kpi mt-auto')
                            ], className='d-flex flex-column')
                        ], id='kpi-grad-rate-card',
                            className='custom-kpi-tile h-100'),

                        # Hover text to show KPI definition
                        dbc.Tooltip(
                            "Statewide average graduation rate across all "
                            "districts for the subgroup 'All Students'",
                            target='kpi-grad-rate-card',
                            placement='bottom')
                    ]),

                    # KPI 2: Median disparity
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                # KPI title
                                html.H5(kpi_median_disparity_title,
                                        className='custom-title',
                                        id='kpi-disparity-title'),
                                # KPI value, handled by callbacks
                                html.H2(kpi_median_disparity,
                                        id="kpi-disparity",
                                        className='custom-kpi mt-auto')
                            ], className='d-flex flex-column')
                        ], id='kpi-disparity-card',
                            className='custom-kpi-tile h-100'),

                        # Hover text to show KPI definition
                        dbc.Tooltip(
                            "Median of district-level graduation rate "
                            "disparities, where disparity = largest "
                            "magnitude graduation rate gap for any subgroup",
                            target='kpi-disparity-card',
                            placement='bottom')
                    ]),

                    # KPI 3: Pct improving
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                # KPI title
                                html.H5(kpi_pct_improving_title,
                                        className='custom-title',
                                        id='kpi-pct-improving-title'),
                                # KPI value, handled by callbacks
                                html.H2(kpi_pct_improving,
                                        id="kpi-pct-improving",
                                        className='custom-kpi mt-auto')

                            ], className='d-flex flex-column')
                        ], id='kpi-pct-improving-card',
                            className='custom-kpi-tile h-100'),

                        # Hover text to show KPI definition
                        dbc.Tooltip(
                            "Percentage of school districts whose graduation "
                            "rate disparity has decreased over the selected "
                            "time range",
                            target='kpi-pct-improving-card',
                            placement='bottom')
                    ]),

                ], className="mb-4"),  # add vertical padding

                html.Hr(),

                # ROW 2: 2 data visualizations
                dbc.Row([

                    # VIZ 1: Line chart of grad rate over time
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H5(viz_line_chart_title,
                                        className='custom-title',
                                        id='grad-rate-line-chart-title'),
                                html.P("Are graduation rates "
                                       "improving over time?",
                                       className='custom-subtitle'),
                                dcc.Graph(
                                    # Graph ID for callbacks
                                    id='grad-rate-line-chart',
                                    figure=viz_line_chart,
                                    # Remove unnecessary interactive features
                                    config={
                                        'displaylogo': False,
                                        'modeBarButtonsToRemove': [
                                            'zoom', 'pan', 'select', 'zoomIn',
                                            'zoomOut', 'autoScale',
                                            'resetScale'
                                        ],
                                        'modeBarButtonsToAdd': [
                                            'downloadJson'
                                        ]
                                    }
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
                                html.H5(viz_dumbbell_chart_title,
                                        className='custom-title',
                                        id='gaps-dumbbell-chart-title'),
                                html.P("Are gaps in student outcomes "
                                       "narrowing over time?",
                                       className='custom-subtitle'),
                                dcc.Graph(
                                    # Graph ID for callbacks
                                    id='gaps-dumbbell-chart',
                                    figure=viz_dumbbell_chart,
                                    # Remove unnecessary interactive features
                                    config={
                                        'displaylogo': False,
                                        'modeBarButtonsToRemove': [
                                            'zoom', 'pan', 'select', 'zoomIn',
                                            'zoomOut', 'autoScale',
                                            'resetScale', 'lasso2d'
                                        ],
                                        'modeBarButtonsToAdd': [
                                            'downloadJson'
                                        ]
                                    }
                                ),
                                html.Div(
                                    '(Gap = subgroup graduation rate - '
                                    'overall graduation rate)',
                                    className='custom-subtitle'
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
                                html.H5(viz_network_chart_title,
                                        className='custom-title',
                                        id='district-network-chart-title'),
                                html.P("Do similar school districts "
                                       "have similar levels of "
                                       "graduation rate disparity?",
                                       className='custom-subtitle'),
                                dcc.Graph(
                                    # Graph ID for callbacks
                                    id='district-network-chart',
                                    figure=viz_network_chart,
                                    # Remove unnecessary interactive features
                                    config={
                                        'displaylogo': False,
                                        'modeBarButtonsToRemove': [
                                            'zoom', 'select', 'lasso2d'
                                        ],
                                        'modeBarButtonsToAdd': [
                                            'downloadJson'
                                        ],
                                        'scrollZoom': True
                                    }
                                ),
                                html.Div(
                                    '(Disparity = largest magnitude graduation'
                                    ' rate gap for any subgroup)',
                                    className='custom-subtitle'
                                )
                            ])
                        ])
                    ])
                ])

            ],
                width=10,  # main body takes up 10 columns or 5/6 of screen
                className="mb-4 px-4"  # add horizontal and vertical padding
            )

        ],
            # Keep both columsn the same height
            # Change overall height based on Container constraints
            className="flex-grow-1 align-items-stretch g-0"
        )
    ],
        style={
            'padding': 0,
            'height': '100vh',  # fill entire vertical height
            'display': 'flex',
            'flexDirection': 'column'
    },
        fluid=True  # container stretches to fill entire width of screen
    )

    return layout
