import math
from collections.abc import Callable

from algorithms.grid_graph import Cell

Heuristic = Callable[[Cell, Cell], float]

MANHATTAN = "Manhattan"
EUCLIDEAN = "Euklidesowa"


def manhattan_distance(cell: Cell, goal: Cell) -> float:
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])


def euclidean_distance(cell: Cell, goal: Cell) -> float:
    return math.hypot(cell[0] - goal[0], cell[1] - goal[1])


HEURISTICS: dict[str, Heuristic] = {
    MANHATTAN: manhattan_distance,
    EUCLIDEAN: euclidean_distance,
}
