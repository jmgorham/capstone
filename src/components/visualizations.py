import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
from src.utils.data_utils import get_disparity_df, get_gaps_df


def get_grad_rate_line_chart(grad_rate_df, district, metric, start_year,
                             stop_year, subgroups):
    # Build list of subgroups to include
    subgroups_to_include = subgroups + ['All Students']

    # Filter data
    grad_rate_filtered_df = grad_rate_df[(
        grad_rate_df['district'] == district) &
        (grad_rate_df['metric'] == metric) &
        (grad_rate_df['year'] >= start_year) &
        (grad_rate_df['year'] <= stop_year) &
        (grad_rate_df['subgroup'].isin(subgroups_to_include))]

    # Build visualization
    fig = px.line(grad_rate_filtered_df, x='year', y='value', color='subgroup',
                  labels={'year': '',
                          'value': f'{metric} (%)',
                          'subgroup': ''})

    # Include x-axis ticks for every year
    fig.update_xaxes(tickmode='array', tickvals=grad_rate_filtered_df['year'])

    # Constrain height of visualization
    fig.update_layout(
        height=500
    )

    # Remove whitespace padding from graph margins
    fig.update_layout(margin={'l': 0, 'r': 0, 't': 0, 'b': 0})

    return fig


def get_disparity_dumbbell_chart(grad_rate_df, district, metric, start_year,
                                 stop_year, subgroups):
    # Build list of subgroups to include
    subgroups_to_include = subgroups + ['All Students']

    # Filter data
    grad_rate_filtered_df = grad_rate_df[(
        grad_rate_df['district'] == district) &
        (grad_rate_df['metric'] == metric) &
        (grad_rate_df['subgroup'].isin(subgroups_to_include))]

    # Calculate gaps from baseline 'All Students'
    gaps_start_year_df = get_gaps_df(grad_rate_filtered_df, metric, start_year)
    gaps_stop_year_df = get_gaps_df(grad_rate_filtered_df, metric, stop_year)

    # Format data for visualization
    dumbbell_data = {"line_x": [],
                     "line_y": [],
                     "start_values": [],
                     "stop_values": []}

    # Loop through subgroups to build out data
    for subgroup in subgroups:
        # Extract gap values in start year and stop year
        gap_start_year = gaps_start_year_df[gaps_start_year_df['subgroup']
                                            == subgroup]['gap'].values[0]
        gap_stop_year = gaps_stop_year_df[gaps_stop_year_df['subgroup']
                                          == subgroup]['gap'].values[0]

        # Add values to lists for start and stop values
        dumbbell_data['start_values'].append(gap_start_year)
        dumbbell_data['stop_values'].append(gap_stop_year)

        # Record x-values for line segment for this subgroup
        dumbbell_data['line_x'].extend([gap_start_year, gap_stop_year, None])

        # Record y-values for line segment for this subgroup
        dumbbell_data['line_y'].extend([subgroup, subgroup, None])

    # Build visualization
    fig = go.Figure(
        data=[

            # Draw line segments for each dumbbell
            go.Scatter(
                x=dumbbell_data['line_x'],
                y=dumbbell_data['line_y'],
                mode='lines',
                showlegend=False,
                marker={'color': "grey"}
            ),

            # Draw point markers for the starting points of each dumbbell
            go.Scatter(
                x=dumbbell_data['start_values'],
                y=subgroups,
                mode='markers',
                name=str(start_year),
                marker={'color': 'green', 'size': 10}
            ),

            # Draw point markers for the stopping points of each dumbbell
            go.Scatter(
                x=dumbbell_data['stop_values'],
                y=subgroups,
                mode='markers',
                name=str(stop_year),
                marker={'color': 'blue', 'size': 10}
            )
        ]
    )

    # Constrain height of visualization
    fig.update_layout(
        height=500,
        legend_itemclick=False
    )

    # Set legend to bottom center of chart
    fig.update_layout(
        legend={
            'orientation': "h",
            'yanchor': "bottom",
            'y': -0.2,
            'xanchor': "center",
            'x': 0.5
        }
    )

    # Remove whitespace padding from graph margins
    fig.update_layout(margin={'l': 0, 'r': 0, 't': 0, 'b': 0})

    return fig


def get_districts_network_chart(grad_rate_df, district, metric, stop_year,
                                subgroups):
    # Filter data
    subgroups_to_include = subgroups + ['All Students']
    grad_rate_filtered_df = grad_rate_df[
        (grad_rate_df['subgroup'].isin(subgroups_to_include))
    ]

    # Calculate disparity data
    dispartiy_df = get_disparity_df(grad_rate_filtered_df, metric, stop_year)

    # Extract values for districts and disparities
    node_districts = dispartiy_df['district'].tolist()
    node_disparity = dispartiy_df['disparity'].tolist()

    # Generate a random geometric graph
    G = nx.random_geometric_graph(len(node_districts), 0.125, seed=0)

    # Format data for visualization

    # Loop through nodes in graph and store position data
    node_x = []
    node_y = []
    for node in G.nodes:
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    # Loop through edges in graph and store position data
    edge_x = []
    edge_y = []
    for edge in G.edges:
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

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
    district_index = node_districts.index(district)
    zoom_x = node_x[district_index]
    zoom_y = node_y[district_index]
    range = 0.2
    fig.update_layout(
        xaxis={'range': [zoom_x - range, zoom_x + range]},
        yaxis={'range': [zoom_y - range, zoom_y + range]}
    )

    return fig
