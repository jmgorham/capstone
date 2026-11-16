"""Component for application callbacks.

This module defines callbacks to dynamically update the dashboard content,
including KPI tiles and data visualizations, whenever the relevant UI filter
selections are changed.
"""

from dash import Input, Output, callback, no_update, exceptions

import src.components.visualizations as viz
from src.components import kpis
from src.utils.sample_data import get_sample_grad_rate_data, get_sample_district_data


# Update KPI 1: Statewide Graduation Rate
# Trigger when metric selection or year selection is changed
@callback(
    Output(component_id='kpi-grad-rate', component_property='children'),
    Output(component_id='kpi-grad-rate-title', component_property='children'),
    Input(component_id='metric-select-radio', component_property='value'),
    Input(component_id='year-range-select', component_property='value'),
    prevent_initial_call=True
)
def update_statewide_grad_rate_kpi(metric, year_range):
    """Callback to update statewide graduation rate KPI tile.

    Args:
        metric (string): metric used to measure graduation rate
        year_range (list[int, int]): range of years included in analysis

    Returns:
        string: formatted KPI text value for statewide graduation rate
        string: descriptive title for KPI including the year
    """
    # Input validation and error handling
    if metric is None or year_range is None:
        raise exceptions.PreventUpdate

    # Get data
    grad_rate_df = get_sample_grad_rate_data()

    # Extract latest year in selected range
    year = year_range[1]

    # Calculate KPI overall statewide grad rate
    overall_grad_rate_kpi_string = kpis.get_statewide_grad_rate(
        grad_rate_df, metric, year)

    # Format KPI title
    kpi_title = kpis.get_statewide_grad_rate_kpi_title(year)

    return overall_grad_rate_kpi_string, kpi_title


# Update KPI 2: Median Graduation Rate Disparity
# Trigger when metric, year, or subgroup selection is changed
@callback(
    Output(component_id='kpi-disparity', component_property='children'),
    Output(component_id='kpi-disparity-title', component_property='children'),
    Input(component_id='metric-select-radio', component_property='value'),
    Input(component_id='year-range-select', component_property='value'),
    Input(component_id='subgroup-select-checklist',
          component_property='value'),
    prevent_initial_call=True
)
def update_median_disparity_kpi(metric, year_range, subgroups):
    """Callback to update median graduation rate disparity KPI tile.

    Arguments:
        metric (string): metric used to measure graduation rate
        year_range (list[int, int]): range of years included in analysis
        subgroups (list<string>): demographic subgroups included in analysis

    Returns:
        string: formatted KPI text value for median graduation rate disparity
        string: descriptive title for KPI including the year
    """
    # Input validation and error handling
    if metric is None or year_range is None or subgroups is None:
        raise exceptions.PreventUpdate

    # Get data
    grad_rate_df = get_sample_grad_rate_data()

    # Extract latest year in selected range
    year = year_range[1]

    # Calculate KPI median grad rate disparity
    median_disparity_kpi_string = kpis.get_median_grad_rate_disparity(
        grad_rate_df, metric, year, subgroups)

    # Format KPI title
    kpi_title = kpis.get_median_grad_rate_disparity_kpi_title(year)

    return median_disparity_kpi_string, kpi_title


# Update KPI 3: Districts Improving Disparity
# Trigger when metric, year, or subgroup selection is changed
@callback(
    Output(component_id='kpi-pct-improving', component_property='children'),
    Output(component_id='kpi-pct-improving-title',
           component_property='children'),
    Input(component_id='metric-select-radio', component_property='value'),
    Input(component_id='year-range-select', component_property='value'),
    Input(component_id='subgroup-select-checklist',
          component_property='value'),
    prevent_initial_call=True
)
def update_districts_improving_kpi(metric, year_range, subgroups):
    """Callback to update percent of districts improving disparity KPI tile.

    Arguments:
        metric (string): metric used to measure graduation rate
        year_range (list[int, int]): range of years included in analysis
        subgroups (list<string>): demographic subgroups included in analysis

    Returns:
        string: formatted KPI text value for percent of districts improving
        string: descriptive title for KPI including the year
    """
    # Input validation and error handling
    if metric is None or year_range is None or subgroups is None:
        raise exceptions.PreventUpdate

    # Get data
    grad_rate_df = get_sample_grad_rate_data()

    # Extract start and stop years from selected range
    start_year = year_range[0]
    stop_year = year_range[1]

    # Calculate KPI pct districts improving disparity
    pct_improving_kpi_string = kpis.get_pct_districts_improving_disparity(
        grad_rate_df, metric, start_year, stop_year, subgroups)

    # Format KPI title
    kpi_title = kpis.get_pct_improving_kpi_title(
        start_year, stop_year)

    return pct_improving_kpi_string, kpi_title


# Update Data Visualization 1: Line Chart, Grad Rates over Time
# Trigger when district, metric, year, or subgroup selection is changed
@callback(
    Output(component_id='grad-rate-line-chart', component_property='figure'),
    Output(component_id='grad-rate-line-chart-title',
           component_property='children'),
    Input(component_id='district-select-dropdown', component_property='value'),
    Input(component_id='metric-select-radio', component_property='value'),
    Input(component_id='year-range-select', component_property='value'),
    Input(component_id='subgroup-select-checklist',
          component_property='value'),
    prevent_initial_call=True
)
def update_grad_rate_line_chart(district, metric, year_range, subgroups):
    """Callback to update graduation rate over time line chart figure.

    Arguments:
        district (string): school district to focus on
        metric (string): metric used to measure graduation rate
        year_range (list[int, int]): range of years included in analysis
        subgroups (list<string>): demographic subgroups included in analysis

    Returns:
        Figure: Plotly figure displaying graduation rate over time line chart
    """
    # Input validation and error handling
    if district is None or metric is None or \
            year_range is None or subgroups is None:
        raise exceptions.PreventUpdate

    # Get data
    grad_rate_df = get_sample_grad_rate_data()

    # Extract start and stop years from selected range
    start_year = year_range[0]
    stop_year = year_range[1]

    # Re-build visualization
    line_chart_fig = viz.get_grad_rate_line_chart(
        grad_rate_df, district, metric, start_year, stop_year, subgroups)

    # Get formatted chart title
    chart_title = viz.get_line_chart_title(district)

    return line_chart_fig, chart_title


# Update Data Visualization 2: Dumbbell Chart, Gaps over Time
# Trigger when district, metric, year, or subgroup selection is changed
@callback(
    Output(component_id='gaps-dumbbell-chart', component_property='figure'),
    Output(component_id='gaps-dumbbell-chart-title',
           component_property='children'),
    Input(component_id='district-select-dropdown', component_property='value'),
    Input(component_id='metric-select-radio', component_property='value'),
    Input(component_id='year-range-select', component_property='value'),
    Input(component_id='subgroup-select-checklist',
          component_property='value'),
    prevent_initial_call=True
)
def update_gaps_dumbbell_chart(district, metric, year_range, subgroups):
    """Callback to update graduation gaps over time dumbbell chart figure.

    Arguments:
        district (string): school district to focus on
        metric (string): metric used to measure graduation rate
        year_range (list[int, int]): range of years included in analysis
        subgroups (list<string>): demographic subgroups included in analysis

    Returns:
        Figure: Plotly figure displaying graduation gaps dumbbell chart
    """
    # Input validation and error handling
    if district is None or metric is None or \
            year_range is None or subgroups is None:
        raise exceptions.PreventUpdate

    # Get data
    grad_rate_df = get_sample_grad_rate_data()

    # Extract start and stop years from selected range
    start_year = year_range[0]
    stop_year = year_range[1]

    # Re-build visualization
    dumbbell_chart_fig = viz.get_disparity_dumbbell_chart(
        grad_rate_df, district, metric, start_year, stop_year, subgroups)

    # Get formatted chart title
    chart_title = viz.get_dumbbell_chart_title(district)

    return dumbbell_chart_fig, chart_title


# Update Data Visualization 3: Network Chart, Similar School Districts
# Trigger when district, metric, year, or subgroup selection is changed
@callback(
    Output(component_id='district-network-chart', component_property='figure'),
    Output(component_id='district-network-chart-title',
           component_property='children'),
    Input(component_id='district-select-dropdown', component_property='value'),
    Input(component_id='metric-select-radio', component_property='value'),
    Input(component_id='year-range-select', component_property='value'),
    Input(component_id='subgroup-select-checklist',
          component_property='value'),
    prevent_initial_call=True
)
def update_districts_network_chart(district, metric, year_range, subgroups):
    """Callback to update districts adjacency network chart figure.

    Arguments:
        district (string): school district to focus on
        metric (string): metric used to measure graduation rate
        year_range (list[int, int]): range of years included in analysis
        subgroups (list<string>): demographic subgroups included in analysis

    Returns:
        Figure: Plotly figure displaying districts adjacency network
    """
    # Input validation and error handling
    if district is None or metric is None or \
            year_range is None or subgroups is None:
        raise exceptions.PreventUpdate

    # Get data
    grad_rate_df = get_sample_grad_rate_data()
    district_df = get_sample_district_data()

    # Extract start and stop years from selected range
    start_year = year_range[0]
    stop_year = year_range[1]

    # Re-build visualization
    network_graph_fig = viz.get_districts_network_chart(
        district_df, grad_rate_df, district, metric, start_year, stop_year,
        subgroups)

    # Get formatted chart title
    chart_title = viz.get_network_chart_title(stop_year)

    return network_graph_fig, chart_title


# Update selected school district when a user clicks on a node (point)
# on Data Visualization 3: Network Chart, Similar School Districts
@callback(
    Output(component_id='district-select-dropdown',
           component_property='value'),
    Input(component_id='district-network-chart',
          component_property='clickData'),
    prevent_initial_call=True
)
def update_selected_district_on_click(click_data):
    # If no point has been clicked, exit without doing anything
    if click_data is None:
        return no_update

    # Extact name of district associated with clicked node
    clicked_district = click_data['points'][0]['customdata'][0]

    return clicked_district
