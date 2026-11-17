"""App component for defining data visualizations.

This module contains functions for creating data visualizations displayed
on the dashboard in order to communicate with data effectively.
"""

import networkx as nx
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors as pc
import numpy as np
import pandas as pd

from src.utils.data_utils import get_disparity_df, get_gaps_df
from src.utils.sorting_utils import sort_subgroups
from src.utils.district_network_utils import get_district_adjacency_graph
from src.utils.district_adjacency_graph import AdjacencyListGraph


def get_grad_rate_line_chart(grad_rate_df, district, metric, start_year,
                             stop_year, subgroups):
    """Create line chart visualization for graduation rates over time.

    The figure displays a time-series line chart with a different series for
    each demogrpahic subgroup, indicating the graduation rate in each year.

    Time complexity: O(N) for N rows of data

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

    # Sort subgroup values for visualization; time complexity of O(NlogN) for
    # N subgroups
    subgroups_sorted = sort_subgroups(subgroups_to_include)

    # Filter data; time complexity of O(N * M) for N rows and M columns
    grad_rate_filtered_df = grad_rate_df[(
        grad_rate_df['district'] == district) &
        (grad_rate_df['metric'] == metric) &
        (grad_rate_df['year'] >= start_year) &
        (grad_rate_df['year'] <= stop_year) &
        (grad_rate_df['subgroup'].isin(subgroups_to_include))]

    # Define colors
    custom_qualitative_palette = px.colors.qualitative.Prism + \
        px.colors.qualitative.Antique[:4] + px.colors.qualitative.Antique[5:]

    # Build visualization
    # Time complexity is O(N) in terms of number of points plotted, where
    # N = (stop_year - start_year) * (# subgroups)
    fig = px.line(grad_rate_filtered_df, x='year', y='value', color='subgroup',
                  # Format axis labels on the chart
                  labels={'year': '',
                          'value': f'{metric} (%)',
                          'subgroup': ''},
                  category_orders={'subgroup': subgroups_sorted},
                  # hover_data allows for accessing columns in hover text
                  hover_data=['subgroup'],
                  # Define color scheme
                  color_discrete_sequence=custom_qualitative_palette)

    # Configure x axis; O(1)
    fig.update_xaxes(
        # Force x-axis ticks for every year
        tickmode='linear',
        tick0=start_year,
        dtick=1
    )

    # Manually draw grid lines; O(N) for N years
    for year in range(start_year, stop_year):
        fig.add_vline(
            x=year,
            line_width=1,
            line_color='LightGray',
            layer='below',
            opacity=1
        )

    # Set custom hover text; O(1)
    fig.update_traces(
        hovertemplate='<b>Subgroup: %{customdata[0]}</b><br><br>' +
        'Year: %{x}<br>' +
        'Grad rate: %{y:.1f}%' +
        '<extra></extra>'
    )

    # Configure layout; O(1)
    fig.update_layout(
        height=500,  # constrain graph height
        margin={'l': 0, 'r': 0, 't': 0, 'b': 0},  # remove whitespace padding
        dragmode=False,  # dragging the mouse should do nothing
        template='simple_white',  # apply minimalist visual style
        font={'family': 'Inter, sans-serif', 'size': 14},  # default font
        hoverlabel={  # configure hover text with font and white background
            'font': {'family': 'Inter, sans-serif', 'size': 14},
            'bgcolor': 'white'}
    )

    return fig


def get_disparity_dumbbell_chart(grad_rate_df, district, metric, start_year,
                                 stop_year, subgroups):
    """Create dumbbell chart for graduation rate gaps over time.

    The figure displays a dumbbell chart. The x-axis indicates the difference
    between a subgroup's graduation rate and the average for all students.
    For each subgroup, one point indicates the disparity in the start year,
    and another point indicates the disparty in the stop year.

    Time complexity: O(N) for N rows of data

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
    # Sorting is O(NlogN) for N subgroups
    subgroups_sorted = sort_subgroups(subgroups)[::-1]

    # Filter data; filtering is O(N * M) for N rows and M columns
    grad_rate_filtered_df = grad_rate_df[(
        grad_rate_df['district'] == district) &
        (grad_rate_df['metric'] == metric) &
        (grad_rate_df['subgroup'].isin(subgroups_to_include))]

    # Calculate gaps from baseline 'All Students'
    # Function get_gaps_df is O(N * M) for N rows and M columns
    gaps_start_year_df = get_gaps_df(grad_rate_filtered_df, metric, start_year)
    gaps_stop_year_df = get_gaps_df(grad_rate_filtered_df, metric, stop_year)

    # Define format for hover text for visualization; O(1)
    gap_definition_text = \
        '<i>Gap = subgroup graduation rate - overall graduation rate</i>'
    hover_template = '<b>Subgroup: %{customdata[0]}</b><br><br>' + \
        'Gap in %{customdata[1]}: %{customdata[2]:.1f}pp<br>' + \
        'Gap in %{customdata[3]}: %{customdata[4]:.1f}pp<br>' + \
        '<b>Gap improving: %{customdata[5]}</b><br><br>' + \
        gap_definition_text + \
        '<extra></extra>'

    # Build visualization
    fig = go.Figure()

    # Loop through subgroups and add data to chart
    # Loop is O(N) for N subgoroups
    for i in range(len(subgroups_sorted)):
        subgroup = subgroups_sorted[i]

        # Extract gap values in start year and stop year
        # Requires filtering with time complexity O(N * M)
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
            marker={'color': '#408c45', 'size': 10},
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
            marker={'color': '#593980', 'size': 10},
            # Add hover text
            customdata=[hover_data],
            hovertemplate=hover_template
        ))

    # Configure x axis; O(1)
    fig.update_xaxes(
        # zeroline=True,  # add vertical grid line at origin
        # zerolinecolor='LightGray',
        tickformat='+'  # format x-axis tick values as signed integers
    )

    # Manually draw vertical line at x = 0; O(1)
    fig.add_vline(
        x=0,
        line_width=1,
        line_color='LightGray',
        opacity=1,
        layer='below'
    )

    # Manually draw horizontal grid lines; O(1)
    for subgroup in subgroups_sorted:
        fig.add_hline(
            y=subgroup,
            line_width=1,
            line_color='LightGray',
            opacity=1,
            layer='below'
        )

    # Configure graph layout; O(1)
    fig.update_layout(
        height=500,  # constrain height
        legend_itemclick=False,
        legend={  # define legend position
            'orientation': "h",
            'yanchor': "bottom",
            'y': 1,
            'xanchor': "center",
            'x': 0.5
        },
        margin={'l': 0, 'r': 0, 't': 0, 'b': 0},  # remove whitespace padding
        dragmode=False,  # dragging the mouse should do nothing
        template='simple_white',  # minimalist visual style
        xaxis_title="Graduation Rate Gap (pp)",  # add x-axis text label
        font={'family': 'Inter, sans-serif', 'size': 14},  # default font
        hoverlabel={  # configure hover text with font and white background
            'font': {'family': 'Inter, sans-serif', 'size': 14},
            'bgcolor': 'white'}
    )

    return fig


def get_districts_network_chart(district_df, grad_rate_df, district, metric,
                                start_year, stop_year, subgroups):
    """Create network chart visualization for similar school districts.

    The figure displays an adjacency graph chart with each school district
    connected to districts similar in characteristics. Each node represents a
    district. Nodes are colored by the graudation rate disparity in each
    district.

    Time complexity: O(N^2) for N rows of data

    Args:
        district_df (DataFrame): data set for school districts
        grad_rate_df (DataFrame): data set for graduation rates
        district (string): school district for focus of analysis
        metric (string): metric used to measure graduation rates
        start_year (int): the minimum year included in analysis
        stop_year (int): the maximum year included in analysis
        subgroups (list<string>): demographic subgroups included in analysis

    Returns:
        Figure: Plotly figure displaying district network chart
    """
    # Filter data; filtering is O(N * M) for N rows and M columns
    subgroups_to_include = subgroups + ['All Students']
    grad_rate_filtered_df = grad_rate_df[
        (grad_rate_df['subgroup'].isin(subgroups_to_include))
    ]
    district_filtered_df = district_df[district_df['year'] == stop_year]

    # Edge case: this graph does not work if 0 subgroups are selected
    if subgroups:

        # Calculate disparity data; vectorized calculations are O(1)
        start_year_disparity_df = get_disparity_df(
            grad_rate_filtered_df, metric, start_year)[['district',
                                                        'disparity']]
        start_year_disparity_df = start_year_disparity_df.rename(
            columns={'disparity': 'disparity_start'})
        stop_year_dispartiy_df = get_disparity_df(
            grad_rate_filtered_df, metric, stop_year)[['district',
                                                       'disparity']]
        stop_year_dispartiy_df = stop_year_dispartiy_df.rename(
            columns={'disparity': 'disparity_stop'})

        # Merge to create 1 disparity data set
        # Inner merge with one-to-one key relationship is O(N) for N rows
        disparity_df = pd.merge(start_year_disparity_df,
                                stop_year_dispartiy_df,
                                how='inner', on='district')
        disparity_df['change'] = disparity_df['disparity_stop'] - \
            disparity_df['disparity_start']
        disparity_df['improving'] = disparity_df['change'] < 0

    else:
        # If there is no data for selected subgroups, create a 'dummy'
        # disparity DataFrame with all 0s for disparity values
        # This is necessary because disparity calculations are not possible
        # given 0 subgroups
        # All vectorized operations here are O(1)
        disparity_df = grad_rate_filtered_df[['district']].drop_duplicates()
        disparity_df['disparity_start'] = np.nan
        disparity_df['disparity_stop'] = np.nan
        disparity_df['improving'] = 'N/A<br>No Subgroups Selected'

    # Get adjacency list graph for districts; O(NlogN) for N rows of data
    district_adjacency_graph = get_district_adjacency_graph(
        district_filtered_df, 5)

    # Extract graph data; O(1)
    district_adjacency_graph_data = district_adjacency_graph.get_adj_list()
    district_metadata = district_adjacency_graph.get_vertex_metadata()

    # Convert to graph object
    # Complexity is O(V + E) for V vertices and E edges
    # In context, this is O(N) for N rows of data, since rows correspond
    # linearly to school districts which correspond linearly to V and E
    G = nx.Graph([(u, v, {'weight': 1 / w})  # inverting weights ensures
                 # for accurate positions, since spring_layout treats larger
                  # values as stronger attractive forces
                  for (u, v,), w in district_adjacency_graph_data.items()])

    # Generate (x, y) coordinates for nodes in graph
    # Time complexity is O(N^2)
    pos = nx.spring_layout(G, weight='weight', seed=0, center=(0, 0))

    # Format data for visualization

    # Loop through nodes in graph, store position data and district metadata
    node_x = []
    node_y = []
    district_names = []
    district_nrc = []
    district_enrollment = []
    district_avg_class_size = []
    district_pct_reduced_lunch = []
    district_expenditures_per_pupil = []
    district_pct_poc_students = []
    district_disparity_start = []
    district_disparity_stop = []
    district_disparity_improving = []
    district_disparity_improving_text = []

    # Time complexity of loop is O(V) for V vertices, or O(N) for N rows
    for node in G.nodes:
        # Record position data
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

        # Record district name
        district_names.append(node)

        # Node values are strings, school district names
        # They can be used to look up school district metadata
        district_vals = district_metadata[node]

        # Extract values for district characteristics from metadata
        district_nrc.append(district_vals['nrc'])
        district_enrollment.append(district_vals['enrollment'])
        district_avg_class_size.append(district_vals['avg_class_size'])
        district_pct_reduced_lunch.append(
            district_vals['pct_reduced_lunch'])
        district_expenditures_per_pupil.append(
            district_vals['expenditures_per_pupil'])
        district_pct_poc_students.append(district_vals['pct_poc_students'])

        # Extract disparity data for the district
        # Requires filtering, which is O(N * M)
        district_disparity_record = \
            disparity_df[disparity_df['district'] == node].iloc[0]
        district_disparity_start.append(
            district_disparity_record['disparity_start'])
        district_disparity_stop.append(
            district_disparity_record['disparity_stop'])
        improving = district_disparity_record['improving']
        district_disparity_improving.append(improving)
        district_disparity_improving_text.append(str(improving).upper())

    # Format data list for including stop_year in custom data for hover text
    stop_year_list = [stop_year] * len(district_names)

    # Loop through edges in graph and store position data
    edge_x = []
    edge_y = []

    # Loop is O(E) for E edges, or O(N) for N rows
    for node1, node2 in G.edges:
        x0, y0 = pos[node1]
        x1, y1 = pos[node2]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    # Define format for custom hover text; O(1)
    hover_template = '<b>%{customdata[0]}</b><br><br>' + \
        '<b>District details (%{customdata[9]})</b><br>' +\
        '- Needs-to-resources category: %{customdata[4]}<br>' +\
        '- Total enrollment: %{customdata[10]:,}<br>' +\
        '- Avg. class size: %{customdata[5]:.1f}<br>' +\
        '- Expenditures per pupil: $%{customdata[7]:.2f}<br>' +\
        '- Pct. students of color: %{customdata[8]:.1f}%<br>' +\
        '- Pct. students eligible for free/reduced lunch: ' +\
        '%{customdata[6]:.1f}%<br>' +\
        '<br>' +\
        'Disparity in ' + str(start_year) + ': %{customdata[1]:.1f}pp<br>' + \
        'Disparity in ' + str(stop_year) + ': %{customdata[2]:.1f}pp<br>' + \
        '<b>Disparity improving: %{customdata[3]}</b><br><br>' + \
        '<i>Disparity = largest magnitude graduation rate gap ' +\
        'for any subgroup</i>' + \
        '<extra></extra>'

    # Define custom color scale; O(1)
    viridis_scale = pc.sequential.Viridis
    custom_continuous_palette = viridis_scale[: int(
        len(viridis_scale) * 0.875)]

    # Conditional styling of nodes; O(N)
    node_sizes = [20 if node == district else 10 for node in district_names]

    # Draw edges; O(E) for E edges or O(N) for N rows
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line={'width': 0.5, 'color': '#808080'},
        hoverinfo='none',
        mode='lines')

    # Draw nodes; O(V) for V vertices or O(N) for N rows
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        marker={
            'showscale': True,
            'colorscale': custom_continuous_palette,
            'color': [],
            'opacity': 0.75,
            'size': node_sizes,
            'colorbar': {
                'thickness': 15,
                'title': {
                    'text': 'Graduation Rate Disparity (pp)',
                    'side': 'right'
                },
                'xanchor': 'left',
            },
            'line': {
                'width': 1,
                'color': 'black'
            }},
        # Add custom hover text - stacking ensures each node has 1 row
        customdata=np.stack(
            (district_names, district_disparity_start,
             district_disparity_stop, district_disparity_improving_text,
             district_nrc, district_avg_class_size, district_pct_reduced_lunch,
             district_expenditures_per_pupil, district_pct_poc_students,
             stop_year_list, district_enrollment),
            axis=1),
        hovertemplate=hover_template
    )

    # Add color to nodes - colored by disparity in latest year
    node_trace.marker.color = district_disparity_stop

    # Build visualization; O(1)
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                    showlegend=False,
                    margin={'b': 0, 'l': 0, 'r': 0, 't': 0},
                    xaxis={'showgrid': False, 'zeroline': False,
                           'showticklabels': False},
                    yaxis={'showgrid': False, 'zeroline': False,
                           'showticklabels': False}),
                    )

    # Configure x axis
    fig.update_xaxes(
        # Hide ticks along the x axis
        showticklabels=False,
        ticks=""
    )

    # Configure y axis
    fig.update_yaxes(
        # Hide ticks along the y axis
        showticklabels=False,
        ticks=""
    )

    # Manually add vertical line at y-axis
    fig.add_shape(
        type='line',
        xref='paper',
        yref='paper',
        x0=0,
        x1=0,
        y0=0,
        y1=1,
        line={'color': 'black', 'width': 1},
        layer='above',
        opacity=1
    )

    # Manually add horizontal line at x-axis
    fig.add_shape(
        type='line',
        xref='paper',
        yref='paper',
        x0=0,
        x1=1,
        y0=0,
        y1=0,
        line={'color': 'black', 'width': 1},
        layer='above',
        opacity=1
    )

    # Math for zooming in on a selected district
    district_index = district_names.index(district)
    zoom_x = node_x[district_index]
    zoom_y = node_y[district_index]
    range_x = 0.15
    range_y = range_x / 3.2

    # Configure graph layout
    fig.update_layout(
        # Zoom logic
        xaxis={'range': [zoom_x - range_x, zoom_x + range_x],
               'autorange': False},
        yaxis={'range': [zoom_y - range_y, zoom_y + range_y],
               'autorange': False},
        dragmode='pan',  # dragging with mouse should pan the graph
        template='simple_white',  # minimalist visual style
        font={'family': 'Inter, sans-serif', 'size': 14},  # default font
        hoverlabel={  # configure hover text font and white background
            'font': {'family': 'Inter, sans-serif', 'size': 14},
            'bgcolor': 'white'
        }
    )

    return fig


def get_line_chart_title(district):
    """Format a title for the line chart of graduation rates over time.

    Args:
        district (string): name of school district displayed in the chart

    Returns:
        string: formatted chart title
    """
    return f'Graduation Rate Outcomes by Student \
        Demographic Subgroups, {district}'


def get_dumbbell_chart_title(district):
    """Format a title for the dumbbell chart of grad rate gaps over time.

    Args:
        district (string): name of school district displayed in the chart

    Returns:
        string: formatted chart title
    """
    return f'Graduation Rate Gaps by Student Demographic Subgroups, {district}'


def get_network_chart_title(year):
    """Format a title for the network chart of similar school districts.

    Args:
        year (int): year of focus for analysis

    Returns:
        string: formatted chart title
    """
    return f'School Districts Grouped by District Characteristics, {year}'
