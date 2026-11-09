import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
from src.utils.data_utils import get_disparity_df


def get_init_line_chart(grad_rate_df):
    # Filter data
    grad_rate_filtered_df = grad_rate_df[(grad_rate_df['metric']
                                         == 'Four-Year Graduation Rate') &
                                         (grad_rate_df['district']
                                          == 'Canidae School District')]

    # Build visualization
    fig = px.line(grad_rate_filtered_df, x='year', y='value', color='subgroup',
                  labels={'year': '',
                          'value': 'Four-Year Graduation Rate (%)',
                          'subgroup': ''})

    # Include x-axis ticks for every year
    fig.update_xaxes(tickmode='array', tickvals=grad_rate_filtered_df['year'])

    # Constrain max width of legend
    fig.update_layout(
        legend={
            'entrywidthmode': 'fraction',
            'entrywidth': 0.3}  # 30% of total plot width
    )

    fig.update_layout(
        height=500
    )

    fig.update_layout(margin={'l': 0, 'r': 0, 't': 0, 'b': 0})

    return fig


def get_init_dumbbell_chart(grad_rate_df):
    # Filter data
    grad_rate_filtered_df = grad_rate_df[(grad_rate_df['metric']
                                         == 'Four-Year Graduation Rate') &
                                         (grad_rate_df['district']
                                          == 'Canidae School District')]

    # Calculate difference from overall grad rate for both start and stop year
    years = sorted(grad_rate_df['year'].dropna().unique())
    start_year = min(years)
    stop_year = max(years)

    # Extract baseline values for group 'All Students'
    baseline_start = grad_rate_filtered_df[(grad_rate_filtered_df['subgroup']
                                            == 'All Students') &
                                           (grad_rate_filtered_df['year']
                                            == start_year)]['value'].values[0]
    baseline_stop = grad_rate_filtered_df[(grad_rate_filtered_df['subgroup']
                                           == 'All Students') &
                                          (grad_rate_filtered_df['year']
                                           == stop_year)]['value'].values[0]

    # Filter to include only start and stop years
    grad_rate_filtered_df = grad_rate_filtered_df[
        (grad_rate_filtered_df['year'] == start_year) |
        (grad_rate_filtered_df['year'] == stop_year)]

    # Filter to exclude group 'All Students' (baseline for comparison)
    grad_rate_filtered_df = grad_rate_filtered_df[~(
        grad_rate_filtered_df['subgroup'] == 'All Students')]

    # Calculate disparity from comparison group
    disparity_df = grad_rate_filtered_df.pivot(
        index='subgroup', columns='year', values='value').reset_index()
    disparity_df['start_year_gap'] = disparity_df[start_year] - baseline_start
    disparity_df['stop_year_gap'] = disparity_df[stop_year] - baseline_stop

    # Format data for visualization
    dumbbell_data = {"line_x": [],
                     "line_y": [],
                     "start_year": [],
                     "stop_year": [],
                     "colors": [],
                     "years": [],
                     "subgroups": []}

    subgroups = disparity_df['subgroup'].unique()

    # Loop through subgroups to build out data
    for subgroup in subgroups:
        dumbbell_data['start_year'].extend([
            disparity_df[disparity_df['subgroup'] ==
                         subgroup]['start_year_gap'].values[0]
        ])
        dumbbell_data['stop_year'].extend([
            disparity_df[disparity_df['subgroup'] ==
                         subgroup]['stop_year_gap'].values[0]
        ])
        dumbbell_data['line_x'].extend([
            disparity_df[disparity_df['subgroup'] ==
                         subgroup]['start_year_gap'].values[0],
            disparity_df[disparity_df['subgroup'] ==
                         subgroup]['stop_year_gap'].values[0],
            None
        ])
        dumbbell_data['line_y'].extend([
            subgroup, subgroup, None
        ])

    # Build viz
    fig = go.Figure(
        data=[
            go.Scatter(
                x=dumbbell_data['line_x'],
                y=dumbbell_data['line_y'],
                mode='lines',
                showlegend=False,
                marker={'color': "grey"}
            ),
            go.Scatter(
                x=dumbbell_data['start_year'],
                y=subgroups,
                mode='markers',
                name='Start Year',
                marker={'color': 'green', 'size': 10}
            ),
            go.Scatter(
                x=dumbbell_data['stop_year'],
                y=subgroups,
                mode='markers',
                name='Stop Year',
                marker={'color': 'blue', 'size': 10}
            )
        ]
    )

    fig.update_layout(
        height=500,
        legend_itemclick=False
    )

    fig.update_layout(
        legend={
            'orientation': "h",
            'yanchor': "bottom",
            'y': -0.2,
            'xanchor': "center",
            'x': 0.5
        }
    )

    fig.update_layout(margin={'l': 0, 'r': 0, 't': 0, 'b': 0})

    return fig


def get_init_network_chart_dummy(grad_rate_df):
    # Get disparity data
    disparity_df = get_disparity_df(grad_rate_df, 'Four-Year Graduation Rate',
                                    2025)
    node_districts = disparity_df['district'].tolist()
    node_disparity = disparity_df['disparity'].tolist()
    n_districts = len(node_districts)

    # Generate a random geometric graph
    G = nx.random_geometric_graph(n_districts, 0.125, seed=0)

    # Extract data for visualization
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    # Draw edges
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line={'width': 0.5, 'color': '#888'},
        hoverinfo='none',
        mode='lines')

    # Draw nodes
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker={
            'showscale': True,
            'colorscale': 'Viridis',
            'color': [],
            'size': 10,
            'colorbar': {
                'thickness': 15,
                'title': {
                    'text': 'Graduation Rate Disparity',
                    'side': 'right'
                },
                'xanchor': 'left',
            },
            'line_width': 2})

    # Add color to nodes
    node_trace.marker.color = node_disparity

    # Hover text: district name
    node_trace.text = node_districts

    # Build visualization
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                    showlegend=False,
                    hovermode='closest',
                    margin={'b': 0, 'l': 0, 'r': 0, 't': 0},
                    xaxis={'showgrid': False, 'zeroline': False,
                           'showticklabels': False},
                    yaxis={'showgrid': False, 'zeroline': False,
                           'showticklabels': False})
                    )

    # Zoom in on one school district
    district_index = node_districts.index('Canidae School District')
    zoom_x = node_x[district_index]
    zoom_y = node_y[district_index]
    range = 0.2
    fig.update_layout(
        xaxis={'range': [zoom_x - range, zoom_x + range]},
        yaxis={'range': [zoom_y - range, zoom_y + range]}
    )

    return fig
