import math
from collections.abc import Callable

from algorithms.grid_graph import Cell

Heuristic = Callable[[Cell, Cell], float]

INFLATION_FACTOR = 3


def manhattan_distance(cell: Cell, goal: Cell) -> float:
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])


def euclidean_distance(cell: Cell, goal: Cell) -> float:
    return math.hypot(cell[0] - goal[0], cell[1] - goal[1])


def inflated_manhattan_distance(cell: Cell, goal: Cell) -> float:
    return INFLATION_FACTOR * manhattan_distance(cell, goal)


HEURISTICS: dict[str, Heuristic] = {
    "Manhattan": manhattan_distance,
    "Euklidesowa": euclidean_distance,
    f"Manhattan ×{INFLATION_FACTOR}": inflated_manhattan_distance,
}

ADMISSIBLE_HEURISTICS = ("Manhattan", "Euklidesowa")
