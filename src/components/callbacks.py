"""Component for application callbacks.

This module defines callbacks to dynamically update the dashboard content,
including KPI tiles and data visualizations, whenever the relevant UI filter
selections are changed.
"""

from dash import Input, Output, callback

import src.components.visualizations as viz
from src.components import kpis
from src.utils.sample_data import get_sample_grad_rate_data


# Update KPI 1: Statewide Graduation Rate
# Trigger when metric selection or year selection is changed
@callback(
    Output(component_id='kpi-grad-rate', component_property='children'),
    Input(component_id='metric-select-radio', component_property='value'),
    Input(component_id='year-range-select', component_property='value')
)
def update_statewide_grad_rate_kpi(metric, year_range):
    """Callback to update statewide graduation rate KPI tile.

    Args:
        metric (string): metric used to measure graduation rate
        year_range (list[int, int]): range of years included in analysis

    Returns:
        string: formatted KPI text value for statewide graduation rate    
    """
    # Get data
    grad_rate_df = get_sample_grad_rate_data()

    # Extract latest year in selected range
    year = year_range[1]

    # Calculate KPI overall statewide grad rate
    overall_grad_rate = kpis.get_statewide_grad_rate(
        grad_rate_df, metric, year)

    # Format as string
    overall_grad_rate_kpi_string = f'{overall_grad_rate:.1f}%'

    return overall_grad_rate_kpi_string


# Update KPI 2: Median Graduation Rate Disparity
# Trigger when metric, year, or subgroup selection is changed
@callback(
    Output(component_id='kpi-disparity', component_property='children'),
    Input(component_id='metric-select-radio', component_property='value'),
    Input(component_id='year-range-select', component_property='value'),
    Input(component_id='subgroup-select-checklist', component_property='value')
)
def update_median_disparity_kpi(metric, year_range, subgroups):
    """Callback to update median graduation rate disparity KPI tile.

    Arguments:
        metric (string): metric used to measure graduation rate
        year_range (list[int, int]): range of years included in analysis
        subgroups (list<string>): demographic subgroups included in analysis

    Returns:
        string: formatted KPI text value for median graduation rate disparity
    """
    # Get data
    grad_rate_df = get_sample_grad_rate_data()

    # Extract latest year in selected range
    year = year_range[1]

    # Calculate KPI median grad rate disparity
    median_grad_rate_disparity = kpis.get_median_grad_rate_disparity(
        grad_rate_df, metric, year, subgroups)

    # Format as string
    median_disparity_kpi_string = f'{median_grad_rate_disparity:.1f}pp'

    return median_disparity_kpi_string


# Update KPI 3: Districts Improving Disparity
# Trigger when metric, year, or subgroup selection is changed
@callback(
    Output(component_id='kpi-pct-improving', component_property='children'),
    Input(component_id='metric-select-radio', component_property='value'),
    Input(component_id='year-range-select', component_property='value'),
    Input(component_id='subgroup-select-checklist', component_property='value')
)
def update_districts_improving_kpi(metric, year_range, subgroups):
    """Callback to update percent of districts improving disparity KPI tile.

    Arguments:
        metric (string): metric used to measure graduation rate
        year_range (list[int, int]): range of years included in analysis
        subgroups (list<string>): demographic subgroups included in analysis

    Returns:
        string: formatted KPI text value for percent of districts improving
    """
    # Get data
    grad_rate_df = get_sample_grad_rate_data()

    # Extract start and stop years from selected range
    start_year = year_range[0]
    stop_year = year_range[1]

    # Calculate KPI pct districts improving disparity
    pct_improving = kpis.get_pct_districts_improving_disparity(
        grad_rate_df, metric, start_year, stop_year, subgroups)

    # Format as string
    pct_improving_kpi_string = f'{pct_improving:.1f}%'

    return pct_improving_kpi_string


# Update Data Visualization 1: Line Chart, Grad Rates over Time
# Trigger when district, metric, year, or subgroup selection is changed
@callback(
    Output(component_id='grad-rate-line-chart', component_property='figure'),
    Input(component_id='district-select-dropdown', component_property='value'),
    Input(component_id='metric-select-radio', component_property='value'),
    Input(component_id='year-range-select', component_property='value'),
    Input(component_id='subgroup-select-checklist', component_property='value')
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
    # Get data
    grad_rate_df = get_sample_grad_rate_data()

    # Extract start and stop years from selected range
    start_year = year_range[0]
    stop_year = year_range[1]

    # Re-build visualization
    line_chart_fig = viz.get_grad_rate_line_chart(
        grad_rate_df, district, metric, start_year, stop_year, subgroups)

    return line_chart_fig


# Update Data Visualization 2: Dumbbell Chart, Gaps over Time
# Trigger when district, metric, year, or subgroup selection is changed
@callback(
    Output(component_id='gaps-dumbbell-chart', component_property='figure'),
    Input(component_id='district-select-dropdown', component_property='value'),
    Input(component_id='metric-select-radio', component_property='value'),
    Input(component_id='year-range-select', component_property='value'),
    Input(component_id='subgroup-select-checklist', component_property='value')
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
    # Get data
    grad_rate_df = get_sample_grad_rate_data()

    # Extract start and stop years from selected range
    start_year = year_range[0]
    stop_year = year_range[1]

    # Re-build visualization
    dumbbell_chart_fig = viz.get_disparity_dumbbell_chart(
        grad_rate_df, district, metric, start_year, stop_year, subgroups)

    return dumbbell_chart_fig


# Update Data Visualization 3: Network Chart, Similar School Districts
# Trigger when district, metric, year, or subgroup selection is changed
@callback(
    Output(component_id='district-network-chart', component_property='figure'),
    Input(component_id='district-select-dropdown', component_property='value'),
    Input(component_id='metric-select-radio', component_property='value'),
    Input(component_id='year-range-select', component_property='value'),
    Input(component_id='subgroup-select-checklist', component_property='value')
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
    # Get data
    grad_rate_df = get_sample_grad_rate_data()

    # Extract start and stop years from selected range
    start_year = year_range[0]
    stop_year = year_range[1]

    # Re-build visualization
    network_graph_fig = viz.get_districts_network_chart(
        grad_rate_df, district, metric, start_year, stop_year, subgroups)

    return network_graph_fig
