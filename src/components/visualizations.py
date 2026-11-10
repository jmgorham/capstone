"""App component for defining data visualizations.

This module contains functions for creating data visualizations displayed
on the dashboard in order to communicate with data effectively.
"""

import networkx as nx
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

from src.utils.data_utils import get_disparity_df, get_gaps_df
from src.utils.sorting_utils import sort_subgroups


def get_grad_rate_line_chart(grad_rate_df, district, metric, start_year,
                             stop_year, subgroups):
    """Create line chart visualization for graduation rates over time.

    The figure displays a time-series line chart with a different series for
    each demogrpahic subgroup, indicating the graduation rate in each year.

    Args:
        grad_rate_df (DataFrame): data set for graduation rates
        district (string): school district for focus of analysis
        metric (string): metric used to measure graduation rates
        start_year (int): the minimum year included in analysis
        stop_year (int): the maximum year included in analysis
        subgroups (list<string>): demographic subgroups included in analysis

    Returns:
        Figure: Plotly figure displaying graduation rates line chart
    """
    # Build list of subgroups to include, with 'All Students' as a baseline
    subgroups_to_include = subgroups + ['All Students']

    # Sort subgroup values for visualization
    subgroups_sorted = sort_subgroups(subgroups_to_include)

    # Filter data
    grad_rate_filtered_df = grad_rate_df[(
        grad_rate_df['district'] == district) &
        (grad_rate_df['metric'] == metric) &
        (grad_rate_df['year'] >= start_year) &
        (grad_rate_df['year'] <= stop_year) &
        (grad_rate_df['subgroup'].isin(subgroups_to_include))]

    # Build visualization
    fig = px.line(grad_rate_filtered_df, x='year', y='value', color='subgroup',
                  # Format axis labels on the chart
                  labels={'year': '',
                          'value': f'{metric} (%)',
                          'subgroup': ''},
                  category_orders={'subgroup': subgroups_sorted},
                  # hover_data allows for accessing columns in hover text
                  hover_data=['subgroup'])

    # Include x-axis ticks for every year
    fig.update_xaxes(tickmode='array', tickvals=grad_rate_filtered_df['year'])

    # Constrain height of visualization
    fig.update_layout(height=500)

    # Remove whitespace padding from graph margins
    fig.update_layout(margin={'l': 0, 'r': 0, 't': 0, 'b': 0})

    # Set custom hover text
    fig.update_traces(
        hovertemplate='<b>%{customdata[0]}</b><br><br>' +
        'Year: %{x}<br>' +
        'Grad rate: %{y:.1f}%' +
        '<extra></extra>'
    )

    # Change hover text background to white
    fig.update_layout(hoverlabel={'bgcolor': 'white'})

    # Disable default legend click behaviors
    fig.update_layout(
        legend={
            'itemclick': False,
            'itemdoubleclick': False
        }
    )

    # Dragging the mouse should do nothing
    fig.update_layout(dragmode=False)

    return fig


def get_disparity_dumbbell_chart(grad_rate_df, district, metric, start_year,
                                 stop_year, subgroups):
    """Create dumbbell chart for graduation rate gaps over time.

    The figure displays a dumbbell chart. The x-axis indicates the difference
    between a subgroup's graduation rate and the average for all students.
    For each subgroup, one point indicates the disparity in the start year,
    and another point indicates the disparty in the stop year.

    Args:
        grad_rate_df (DataFrame): data set for graduation rates
        district (string): school district for focus of analysis
        metric (string): metric used to measure graduation rates
        start_year (int): the minimum year included in analysis
        stop_year (int): the maximum year included in analysis
        subgroups (list<string>): demographic subgroups included in analysis

    Returns:
        Figure: Plotly figure displaying grad rate gaps dumbbell chart
    """
    # Build list of subgroups to include in data transformations
    subgroups_to_include = subgroups + ['All Students']

    # Sort subgroup values for visualization
    # Reverse the list since the chart is constructed from the bottom up
    subgroups_sorted = sort_subgroups(subgroups)[::-1]

    # Filter data
    grad_rate_filtered_df = grad_rate_df[(
        grad_rate_df['district'] == district) &
        (grad_rate_df['metric'] == metric) &
        (grad_rate_df['subgroup'].isin(subgroups_to_include))]

    # Calculate gaps from baseline 'All Students'
    gaps_start_year_df = get_gaps_df(grad_rate_filtered_df, metric, start_year)
    gaps_stop_year_df = get_gaps_df(grad_rate_filtered_df, metric, stop_year)

    # Define format for hover text for visualization
    gap_definition_text = \
        'Gap = subgroup grad rate - overall grad rate'
    hover_template = '<b>%{customdata[0]}</b><br><br>' + \
        'Gap in %{customdata[1]}: %{customdata[2]:.1f}pp<br>' + \
        'Gap in %{customdata[3]}: %{customdata[4]:.1f}pp<br>' + \
        '<b>Gap improving: %{customdata[5]}</b><br><br>' + \
        gap_definition_text + \
        '<extra></extra>'

    # Build visualization
    fig = go.Figure()

    # Loop through subgroups and add data to chart
    for i in range(len(subgroups_sorted)):
        subgroup = subgroups_sorted[i]

        # Extract gap values in start year and stop year
        gap_start_year = gaps_start_year_df[gaps_start_year_df['subgroup']
                                            == subgroup]['gap'].values[0]
        gap_stop_year = gaps_stop_year_df[gaps_stop_year_df['subgroup']
                                          == subgroup]['gap'].values[0]

        # Build custom data used for hover text
        gap_change = gap_stop_year - gap_start_year
        hover_data = [subgroup, start_year, gap_start_year, stop_year,
                      gap_stop_year, str((gap_change) > 0).upper()]

        # Draw line segments for the dumbbell
        fig.add_trace(go.Scatter(
            x=[gap_start_year, gap_stop_year],
            y=[subgroup, subgroup],
            mode='lines',
            showlegend=False,
            marker={'color': "grey"},
            # Add hover text
            customdata=[hover_data, hover_data],
            hovertemplate=hover_template
        ))

        # Draw point marker for the starting point of the dumbbell
        fig.add_trace(go.Scatter(
            x=[gap_start_year],
            y=[subgroup],
            mode='markers',
            name=str(start_year),
            showlegend=(i == 0),  # draw legend exactly once
            marker={'color': 'green', 'size': 10},
            # Add hover text
            customdata=[hover_data],
            hovertemplate=hover_template
        ))

        # Draw point marker for the stopping point of the dumbbell
        fig.add_trace(go.Scatter(
            x=[gap_stop_year],
            y=[subgroup],
            mode='markers',
            name=str(stop_year),
            showlegend=(i == 0),  # draw legend exactly once
            marker={'color': 'blue', 'size': 10},
            # Add hover text
            customdata=[hover_data],
            hovertemplate=hover_template
        ))

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

    # Change hover text background to white
    fig.update_layout(hoverlabel={'bgcolor': 'white'})

    # Dragging the mouse should do nothing
    fig.update_layout(dragmode=False)

    return fig


def get_districts_network_chart(grad_rate_df, district, metric, start_year,
                                stop_year, subgroups):
    """Create network chart visualization for similar school districts.

    The figure displays an adjacency graph chart with each school district
    connected to districts similar in characteristics. Each node represents a
    district. Nodes are colored by the graudation rate disparity in each
    district.

    Args:
        grad_rate_df (DataFrame): data set for graduation rates
        district (string): school district for focus of analysis
        metric (string): metric used to measure graduation rates
        start_year (int): the minimum year included in analysis
        stop_year (int): the maximum year included in analysis
        subgroups (list<string>): demographic subgroups included in analysis

    Returns:
        Figure: Plotly figure displaying district network chart
    """
    # Filter data
    subgroups_to_include = subgroups + ['All Students']
    grad_rate_filtered_df = grad_rate_df[
        (grad_rate_df['subgroup'].isin(subgroups_to_include))
    ]

    # Calculate disparity data
    start_year_disparity_df = get_disparity_df(
        grad_rate_filtered_df, metric, start_year)[['district', 'disparity']]
    start_year_disparity_df = start_year_disparity_df.rename(
        columns={'disparity': 'disparity_start'})
    stop_year_dispartiy_df = get_disparity_df(
        grad_rate_filtered_df, metric, stop_year)[['district', 'disparity']]
    stop_year_dispartiy_df = stop_year_dispartiy_df.rename(
        columns={'disparity': 'disparity_stop'})

    # Merge to create 1 disparity data set
    disparity_df = pd.merge(start_year_disparity_df,
                            stop_year_dispartiy_df, how='inner', on='district')
    disparity_df['change'] = disparity_df['disparity_stop'] - \
        disparity_df['disparity_start']
    disparity_df['improving'] = disparity_df['change'] < 0

    # Extract values for districts and disparities
    node_districts = disparity_df['district'].tolist()
    node_disparity_start = disparity_df['disparity_start'].tolist()
    node_disparity_stop = disparity_df['disparity_stop'].tolist()
    node_disparity_improving = disparity_df['improving'].tolist()
    node_improving_text = [str(val).upper()
                           for val in node_disparity_improving]

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

    # Define format for custom hover text
    hover_template = '<b>%{customdata[0]}</b><br><br>' + \
        'Enrollment: XXXX<br>Funding: XXXX<br>' + \
        'Student/teacher ratio: XXXX<br><br>' + \
        'Disparity in ' + str(start_year) + ': %{customdata[1]:.1f}pp<br>' + \
        'Disparity in ' + str(stop_year) + ': %{customdata[2]:.1f}pp<br>' + \
        '<b>Disparity improving: %{customdata[3]}</b><br><br>' + \
        'Disparity = max grad rate gap for any subgroup' + \
        '<extra></extra>'

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
        marker={
            'showscale': True,
            'colorscale': 'Viridis',
            'color': [],
            'size': 10,
            'colorbar': {
                'thickness': 15,
                'title': {
                    'text': f'Graduation Rate Disparity ({stop_year})',
                    'side': 'right'
                },
                'xanchor': 'left',
            },
            'line_width': 2},
        # Add custom hover text - stacking ensures each node has 1 row
        customdata=np.stack(
            (node_districts, node_disparity_start,
             node_disparity_stop, node_improving_text),
            axis=1),
        hovertemplate=hover_template
    )

    # Add color to nodes - colored by disparity in latest year
    node_trace.marker.color = node_disparity_stop

    # Build visualization
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                    showlegend=False,
                    margin={'b': 0, 'l': 0, 'r': 0, 't': 0},
                    xaxis={'showgrid': False, 'zeroline': False,
                           'showticklabels': False},
                    yaxis={'showgrid': False, 'zeroline': False,
                           'showticklabels': False}),
                    )

    # Zoom in on the selected school district
    district_index = node_districts.index(district)
    zoom_x = node_x[district_index]
    zoom_y = node_y[district_index]
    range = 0.2
    fig.update_layout(
        xaxis={'range': [zoom_x - range, zoom_x + range], 'autorange': False},
        yaxis={'range': [zoom_y - range, zoom_y + range], 'autorange': False}
    )

    # Change hover text background to white
    fig.update_layout(hoverlabel={'bgcolor': 'white'})

    # Dragging with mouse should pan the graph
    fig.update_layout(dragmode='pan')

    return fig
