"""Euclidean distance computation module."""

import math
from src.models import Point


def euclidean_distance(p1: Point, p2: Point) -> float:
    """Compute standard 2D Euclidean distance between two Points.

    Formula: sqrt((x2 - x1)^2 + (y2 - y1)^2)
    """
    return math.hypot(p2.x - p1.x, p2.y - p1.y)
