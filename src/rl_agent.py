"""Beginner-friendly route policy interface for future Q-learning work."""


def choose_route(routes):
    """Choose the lowest-cost route; this is a baseline, not trained RL."""
    return routes.loc[routes["eco_score"].idxmin()]
