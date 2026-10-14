"""Unit tests for OpenStreetMap graph utilities."""

import networkx as nx
import pytest
from src.osm_graph import load_graph, route_nodes, route_summary


@pytest.fixture
def mini_graph():
    """Create a lightweight synthetic graph matching OSMnx edge schemas."""
    G = nx.MultiDiGraph()
    G.graph["crs"] = "epsg:4326"

    # Add 3 nodes with coordinates
    G.add_node(1, y=9.9982, x=76.3073)
    G.add_node(2, y=10.1076, x=76.3570)
    G.add_node(3, y=10.5276, x=76.2144)

    # Add edges with length (meters) and travel_time (seconds)
    G.add_edge(1, 2, length=15000.0, travel_time=1200.0)
    G.add_edge(2, 3, length=65000.0, travel_time=4800.0)
    return G


def test_osm_mini_graph_routing(mini_graph):
    # Shortest path from node 1 to 3
    nodes = nx.shortest_path(mini_graph, 1, 3, weight="length")
    assert nodes == [1, 2, 3]

    # Coordinates summary extraction
    coords = [(mini_graph.nodes[n]["y"], mini_graph.nodes[n]["x"]) for n in nodes]
    assert len(coords) == 3
    assert coords[0] == (9.9982, 76.3073)
    assert coords[-1] == (10.5276, 76.2144)
