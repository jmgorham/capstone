"""Data structure implementation for an unweighted non-directional adjacency
list graph."""

from collections import defaultdict


class AdjacencyListGraph:
    """Represent an unweighted non-directional adjacency list graph.

    Contains vertices represeted by a vertex id and vertex metadata. Edges
    between vertices represent that the two vertices are mutually adjacent
    within the graph.

    Attributes:
        adj_list (dict<string: list[string]>): representation of the
            adjacency list graph as a dictionary mapping vertex ids to lists
            of adjacent vertex ids
        vertex_metadata (dict<string: dict>): detailed metadata on vertices
            with vertex ids mapped to json-like dictionaries containing
            vertex metadata
    """

    def __init__(self):
        """Initialize a new AdjacencyListGraph instance."""
        # This dictionary will map vertices to lists of adjacent vertices
        self.adj_list = defaultdict(list)

        # This dictionary will map vertices to metadata about the vertices
        self.vertex_metadata = {}

    def add_vertex(self, vertex_id, vertex_metadata):
        """Add a vertex to an AdjacencyListGraph.

        Args:
            vertex_id (string): text to uniquely identify the vertex to add
            vertex_metadata (dict): json-like metadata for the vertex
        """
        # Check if vertex already exists in the list
        if vertex_id not in self.vertex_metadata:
            # Register vertex metadata
            self.vertex_metadata[vertex_id] = vertex_metadata

            # Add to graph with 0 edges
            self.adj_list[vertex_id] = []

    def add_edge(self, vertex_id_0, vertex_metadata_0,
                 vertex_id_1, vertex_metadata_1):
        """Add an edge between two vertices in an AdjacencyListGraph.

        Args:
            vertex_id_0 (string): text to uniquely identify the first vertex
            vertex_metadata_0 (dict): json-like metadata for the first vertex
            vertex_id_1 (string): text to uniquely identify the second vertex
            vertex_metadata_1 (dict): json-like metadata for the second vertex
        """
        # Ensure both vertices exist in the graph
        self.add_vertex(vertex_id_0, vertex_metadata_0)
        self.add_vertex(vertex_id_1, vertex_metadata_1)

        # Add edge from vertex 0 to vertex 1
        if vertex_id_1 not in self.adj_list[vertex_id_0]:
            self.adj_list[vertex_id_0].append(vertex_id_1)

        # Add edge from vertex 1 to vertex 0
        if vertex_id_0 not in self.adj_list[vertex_id_1]:
            self.adj_list[vertex_id_1].append(vertex_id_0)

    def get_adj_list(self):
        """Get the data representation of the AdjacencyListGraph vertices and
        edge mappings.

        Returns:
            adj_list (dict<string: list[string]>): representation of the
                adjacency list graph as a dictionary mapping vertex ids to
                lists of adjacent vertex ids
        """
        return self.adj_list

    def get_vertex_metadata(self):
        """Get metadata for all vertices in the AdjacencyListGraph.

        Returns:
            vertex_metadata (dict<string: dict>): detailed metadata on vertices
                with vertex ids mapped to json-like dictionaries containing
                vertex metadata
        """
        return self.vertex_metadata
