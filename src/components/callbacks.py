from dash import callback, Output, Input
from src.utils.sample_data import get_sample_grad_rate_data
import src.components.kpis as kpis


# Update KPI 1: Statewide Graduation Rate
# Trigger when metric selection or year selection is changed
@callback(
    Output(component_id='kpi-grad-rate', component_property='children'),
    Input(component_id='metric-select-radio', component_property='value'),
    Input(component_id='year-range-select', component_property='value')
)
def update_statewide_grad_rate_kpi(metric, year_range):
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
