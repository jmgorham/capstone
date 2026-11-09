import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import networkx as nx


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
                          'subgroup': ''},
                  title='Graduation Rates over Time')

    # Include x-axis ticks for every year
    fig.update_xaxes(tickmode='array', tickvals=grad_rate_filtered_df['year'])

    # Constrain max width of legend
    fig.update_layout(
        legend={
            'entrywidthmode': 'fraction',
            'entrywidth': 0.3}  # 30% of total plot width
    )

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
        title={'text': 'Graduation Rate Gaps over Time'},
        height=1000,
        legend_itemclick=False
    )

    return fig


def get_dummy_dumbbell_chart():
    # Create sample data
    data = {
        "year": [2020, 2021, 2022, 2023, 2024, 2025] * 3,
        "value": [70.0, 73.2, 74.5, 77.8, 80.1, 80.5, 65.8, 66.7, 68.9, 70.2,
                  73.4, 75.5, 50.3, 54.4, 55.5, 58.8, 57.5, 59.3],
        "subgroup": ['subgroup 1'] * 6 + ['subgroup 2'] * 6 +
        ['subgroup 3'] * 6
    }
    df = pd.DataFrame(data)

    # Reference: https://plotly.com/python/dumbbell-plots/
    df_dumbbell = {"line_x": [],
                   "line_y": [],
                   "2020": [],
                   "2025": [],
                   "colors": [],
                   "years": [],
                   "subgroups": []}

    subgroups = df['subgroup'].unique()

    for subgroup in subgroups:
        df_dumbbell['2020'].extend(
            [df.loc[(df.year == 2020) &
                    (df.subgroup == subgroup)]['value'].values[0]])
        df_dumbbell['2025'].extend(
            [df.loc[(df.year == 2025) &
                    (df.subgroup == subgroup)]['value'].values[0]])
        df_dumbbell['line_x'].extend(
            [
                df.loc[(df.year == 2020) &
                       (df.subgroup == subgroup)]['value'].values[0],
                df.loc[(df.year == 2025) &
                       (df.subgroup == subgroup)]['value'].values[0],
                None
            ]
        )
        df_dumbbell['line_y'].extend([subgroup, subgroup, None])

        fig = go.Figure(
            data=[
                go.Scatter(
                    x=df_dumbbell['line_x'],
                    y=df_dumbbell['line_y'],
                    mode='lines',
                    showlegend=False,
                    marker=dict(color="grey")
                ),
                go.Scatter(
                    x=df_dumbbell['2020'],
                    y=subgroups,
                    mode='markers',
                    name='2020',
                    marker=dict(color='green', size=10)
                ),
                go.Scatter(
                    x=df_dumbbell['2025'],
                    y=subgroups,
                    mode='markers',
                    name='2025',
                    marker=dict(color='blue', size=10)
                )
            ]
        )

    return fig


def get_dummy_network_chart():
    # https://plotly.com/python/network-graphs/
    G = nx.random_geometric_graph(200, 0.125)
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

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title=dict(
                    text='Node Connections',
                    side='right'
                ),
                xanchor='left',
            ),
            line_width=2))

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: '+str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                    title=dict(
                        text="<br>Network graph made with Python",
                        font=dict(
                            size=16
                        )
                    ),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    annotations=[dict(
                        text="Python code: <a href='https://plotly.com/python/network-graphs/'> https://plotly.com/python/network-graphs/</a>",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002)],
                    xaxis=dict(showgrid=False, zeroline=False,
                               showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    return fig
