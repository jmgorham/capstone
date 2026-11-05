import dash_bootstrap_components as dbc
from dash import Dash, html
from src.components.layout import create_layout

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = create_layout()

if __name__ == '__main__':
    app.run(debug=True)