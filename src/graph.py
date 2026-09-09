"""Small NetworkX adapter for route graph experiments."""


def build_route_graph(routes):
    """Build a directed graph from route rows when NetworkX is installed."""
    import networkx as nx

    graph = nx.DiGraph()
    for _, route in routes.iterrows():
        stops = [stop.strip() for stop in route["route_name"].split("-")]
        for start, end in zip(stops, stops[1:]):
            graph.add_edge(start, end, route_id=route["route_id"], distance_km=route["distance_km"])
    return graph
