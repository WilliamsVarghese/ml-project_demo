"""OpenStreetMap road-network download and route helpers."""

from pathlib import Path

import networkx as nx
import osmnx as ox


def geocode_place(place, region="Kerala, India"):
    """Return (latitude, longitude) from OpenStreetMap's geocoder."""
    return ox.geocode(f"{place}, {region}")


def download_drive_graph(source, destination, output_path, region="Kerala, India", padding_degrees=0.12):
    """Download and save the real drivable OSM network around two places."""
    source_lat, source_lon = geocode_place(source, region)
    destination_lat, destination_lon = geocode_place(destination, region)
    north = max(source_lat, destination_lat) + padding_degrees
    south = min(source_lat, destination_lat) - padding_degrees
    east = max(source_lon, destination_lon) + padding_degrees
    west = min(source_lon, destination_lon) - padding_degrees

    graph = ox.graph.graph_from_bbox(
        bbox=(west, south, east, north),
        network_type="drive",
        simplify=True,
    )
    graph = ox.routing.add_edge_speeds(graph)
    graph = ox.routing.add_edge_travel_times(graph)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ox.io.save_graphml(graph, filepath=output_path)
    return graph


def load_graph(graph_path):
    """Load a previously downloaded OSM graph."""
    return ox.io.load_graphml(filepath=graph_path)


def route_nodes(graph, source, destination, weight="length"):
    """Find the shortest real-network route using an OSM edge attribute."""
    source_lat, source_lon = geocode_place(source)
    destination_lat, destination_lon = geocode_place(destination)
    source_node = ox.distance.nearest_nodes(graph, source_lon, source_lat)
    destination_node = ox.distance.nearest_nodes(graph, destination_lon, destination_lat)
    return nx.shortest_path(graph, source_node, destination_node, weight=weight)


def route_summary(graph, nodes):
    """Summarize distance, travel time, and coordinates for a graph route."""
    edges = ox.routing.route_to_gdf(graph, nodes)
    return {
        "distance_km": float(edges["length"].sum() / 1000),
        "travel_time_min": float(edges["travel_time"].sum() / 60),
        "coordinates": [(graph.nodes[node]["y"], graph.nodes[node]["x"]) for node in nodes],
        "edge_count": len(edges),
    }
