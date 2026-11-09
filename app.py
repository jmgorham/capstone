import dash_bootstrap_components as dbc
from dash import Dash, html
from src.components.layout import create_layout
from src.utils.sample_data import get_sample_grad_rate_data
import src.components.callbacks

# Initialize application
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load data
grad_rate_df = get_sample_grad_rate_data()

# Build dashboard
app.layout = create_layout(grad_rate_df)

if __name__ == '__main__':
    app.run(debug=True)
