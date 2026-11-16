"""Utilities for managing network graphs of school districts.

This module provides functions for using algorithms and data structures to
build adjacency graph networks of similar school districts.
"""


import numpy as np
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

from src.utils.district_adjacency_graph import AdjacencyListGraph


def get_district_adjacency_graph(district_filtered_df, k):
    """Create an adjacency graph connecting similar school districts.

    Uses a custom AdjacencyListGraph data structure and a k-nearest neighbors
    model to draw edges between similar districts. For each district, a
    non-directed edge is drawn between that district and each of its
    k-nearest neighbors.

    Args:
        district_filtered_df (DataFrame): school district data, filtered to 
            include exactly 1 year of data and 1 row per school district
        k (int): minimum number of edges to draw for each district

    Returns:
        AdjacencyListGraph: adjacency graph network containing district
            vertex and edge data
    """
    # The data set must contain exactly 1 year and exactly 1 row per school
    # district; otherwise, these algorithms will break
    if district_filtered_df['year'].nunique() != 1 or not \
            district_filtered_df['district'].is_unique:
        # Return an empty adjacency list graph and exit the function
        return AdjacencyListGraph()

    # Filter out 'Statewide' value
    district_filtered_df = district_filtered_df[
        district_filtered_df['district'] != 'Statewide School District']

    # Initialize adjacency graph
    adjacency_list_graph = AdjacencyListGraph()

    # Fit KNN model
    _, indices = fit_district_k_nearest_neighbors(
        district_filtered_df, k)

    # Iterate through districts
    for i in range(len(indices)):
        # indices is a list of lists; each list has k+1 elements with a
        # district index as the first value and indexes of adjacent districts
        # as the other values
        # indices are in the same order as district_filtered_df

        # Extract values
        indices_row = indices[i]
        district_index = indices_row[0]
        adjacent_district_indexes = indices_row[1:]

        # Extract district data associated with district_index
        district_record = district_filtered_df.iloc[district_index].to_dict()
        district_name = district_record['district']

        # Add edges to graph
        for adj_district_index in adjacent_district_indexes:

            # Extract district data associated with adj_district_index
            adj_district_record = \
                district_filtered_df.iloc[adj_district_index].to_dict()
            adj_district_name = adj_district_record['district']

            # Add edge between districts, including district data
            adjacency_list_graph.add_edge(district_name, district_record,
                                          adj_district_name,
                                          adj_district_record)

    return adjacency_list_graph


def fit_district_k_nearest_neighbors(district_filtered_df, k):
    """Fit a k-nearest neighbors model to school district data.

    Calculates the Euclidean district between each school district according to
    district characteristics, and determines the k districts nearest to each
    district.

    Args:
        district_filtered_df (DataFrame): school district data, filtered to 
            include exactly 1 year of data and 1 row per school district
        k (int): number of nearest neighbors to calculate for each district

    Returns:
        distances (ndarray): the Euclidean distances of each district to each
            of its k-nearest district neighbors
        indices (ndarray): the integer row indices of the k-nearest district
            neighbors to each district, including the district itself as the
            nearest neighbor
            Example: [[0, 2, 5], [1, 2, 7], [2, 6, 3]]
    """
    # Format data for ML
    features_df = district_filtered_df.copy()

    # Remove columns that identify rows
    features_df = features_df.drop(columns=['district', 'year'])

    # Add column for 'high needs' categories
    features_df['high_needs'] = np.where(
        features_df['nrc'].str.contains('High'), 1, 0)

    # Define transformations for columns
    preprocessor = ColumnTransformer(
        transformers=[
            # Min-max normalization for numerical columns
            ('num', MinMaxScaler(),
             make_column_selector(dtype_include=['number'])),
            # One-hot encoding for categorical columns
            ('cat',
             OneHotEncoder(handle_unknown='ignore', sparse_output=False),
             make_column_selector(dtype_include=[
                 'object', 'category', 'string']))
        ],
        remainder='drop'
    ).set_output(transform="pandas")  # format output as DataFrame

    features_transformed_df = preprocessor.fit_transform(features_df)

    features_transformed_df.head()

    # Fit unsupervized K-Nearest Neighbors model
    knn = NearestNeighbors(n_neighbors=k+1,
                           metric='euclidean').fit(features_transformed_df)

    # Extract data on nodes and neighbors
    distances, indices = knn.kneighbors(features_transformed_df)

    return distances, indices
