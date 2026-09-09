"""Lightweight optimizer interface for future route populations."""


def select_best_route(routes):
    """Return the best route according to the existing eco score."""
    return routes.loc[routes["eco_score"].idxmin()]
