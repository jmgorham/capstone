import dash_bootstrap_components as dbc
from dash import Dash, html
from src.components.layout import create_layout
from src.utils.sample_data import get_sample_grad_rate_data, get_sample_district_data
import src.components.callbacks
import pandas as pd

# Configure Pandas behavior
pd.options.mode.copy_on_write = True

# Initialize application
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load data
grad_rate_df = get_sample_grad_rate_data()
district_df = get_sample_district_data()

# Build dashboard
app.layout = create_layout(grad_rate_df, district_df)

if __name__ == '__main__':
    app.run(debug=True)
