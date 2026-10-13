import math

import pytest

from algorithms.grid_graph import GridGraph
from algorithms.heuristics import (
    ADMISSIBLE_HEURISTICS,
    HEURISTICS,
    INFLATION_FACTOR,
    euclidean_distance,
    inflated_manhattan_distance,
    manhattan_distance,
)
from grid_maps import breadth_first_distances, parse_grid


def test_manhattan_distance_sums_row_and_column_differences():
    assert manhattan_distance((0, 0), (3, 4)) == 7
    assert manhattan_distance((5, 2), (1, 6)) == 8


def test_euclidean_distance_is_straight_line_length():
    assert euclidean_distance((0, 0), (3, 4)) == 5
    assert euclidean_distance((1, 1), (2, 2)) == pytest.approx(math.sqrt(2))


def test_inflated_manhattan_multiplies_manhattan_distance():
    assert inflated_manhattan_distance((0, 0), (3, 4)) == INFLATION_FACTOR * 7


@pytest.mark.parametrize("heuristic", HEURISTICS.values(), ids=HEURISTICS.keys())
def test_heuristic_is_zero_at_goal_and_symmetric(heuristic):
    assert heuristic((4, 7), (4, 7)) == 0
    assert heuristic((1, 2), (6, 3)) == heuristic((6, 3), (1, 2))


def test_euclidean_never_exceeds_manhattan():
    cells = [(row, col) for row in range(6) for col in range(6)]

    for cell in cells:
        assert euclidean_distance(cell, (2, 3)) <= manhattan_distance(cell, (2, 3))


@pytest.mark.parametrize("name", ADMISSIBLE_HEURISTICS)
def test_admissible_heuristics_never_overestimate_real_distance(name):
    heuristic = HEURISTICS[name]
    graph, _, goal = parse_grid(
        """
        S...#....
        .##.#.##.
        ..#...#..
        .##.###.#
        ....#...G
        """
    )

    for cell, real_distance in breadth_first_distances(graph, goal).items():
        assert heuristic(cell, goal) <= real_distance


def test_inflated_heuristic_overestimates_on_open_grid():
    graph = GridGraph(5, 5)
    goal = (4, 4)

    real_distances = breadth_first_distances(graph, goal)

    assert inflated_manhattan_distance((0, 0), goal) > real_distances[(0, 0)]
