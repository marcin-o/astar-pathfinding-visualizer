import random
from functools import partial

import pytest

from algorithms.astar import a_star
from algorithms.dijkstra import dijkstra
from algorithms.grid_graph import GridGraph
from algorithms.heuristics import euclidean_distance, manhattan_distance
from grid_maps import assert_valid_path, breadth_first_distances, parse_grid

SEARCHES = {
    "dijkstra": dijkstra,
    "a_star_manhattan": partial(a_star, heuristic=manhattan_distance),
    "a_star_euclidean": partial(a_star, heuristic=euclidean_distance),
}

all_searches = pytest.mark.parametrize("search", SEARCHES.values(), ids=SEARCHES.keys())

MAP_WITH_DETOUR = """
    .....
    .S#G.
    .....
"""

MAP_WITHOUT_PATH = """
    S.#..
    ..#.G
    ..#..
"""

MAP_WITH_MAZE = """
    S...#.......
    .##.#.####..
    ..#...#..#..
    #.#####.##..
    ..#.....#...
    .##.###.#.#.
    ....#.....#G
"""


def random_graph(seed: int, rows: int = 15, cols: int = 20, wall_density: float = 0.3) -> GridGraph:
    rng = random.Random(seed)
    walls = {(row, col) for row in range(rows) for col in range(cols) if rng.random() < wall_density}
    return GridGraph(rows, cols, frozenset(walls - {(0, 0), (rows - 1, cols - 1)}))


@all_searches
def test_finds_straight_path_on_open_grid(search):
    graph, start, goal = parse_grid("S....G")

    result = search(graph, start, goal)

    assert result.path == [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]
    assert result.path_length == 5


@all_searches
def test_goes_around_obstacle(search):
    graph, start, goal = parse_grid(MAP_WITH_DETOUR)

    result = search(graph, start, goal)

    assert_valid_path(graph, result.path, start, goal)
    assert result.path_length == 4


@all_searches
def test_finds_shortest_path_through_maze(search):
    graph, start, goal = parse_grid(MAP_WITH_MAZE)

    result = search(graph, start, goal)

    assert_valid_path(graph, result.path, start, goal)
    assert result.path_length == breadth_first_distances(graph, start)[goal]


@all_searches
def test_reports_missing_path_after_exploring_reachable_area(search):
    graph, start, goal = parse_grid(MAP_WITHOUT_PATH)

    result = search(graph, start, goal)

    assert result.path == []
    assert not result.path_found
    assert result.path_length is None
    assert result.visited_count == 6


@all_searches
def test_start_equal_to_goal_gives_zero_length_path(search):
    graph = GridGraph(4, 4)

    result = search(graph, (2, 1), (2, 1))

    assert result.path == [(2, 1)]
    assert result.path_length == 0
    assert result.visited_count == 1


@all_searches
def test_each_cell_is_visited_at_most_once(search):
    graph = random_graph(seed=7)

    result = search(graph, (0, 0), (14, 19))

    visited = [step.current for step in result.steps]
    assert len(visited) == len(set(visited))


@pytest.mark.parametrize("seed", range(25))
def test_a_star_and_dijkstra_find_paths_of_equal_minimal_length(seed):
    graph = random_graph(seed)
    start, goal = (0, 0), (graph.rows - 1, graph.cols - 1)
    expected_length = breadth_first_distances(graph, start).get(goal)

    dijkstra_result = dijkstra(graph, start, goal)
    manhattan_result = a_star(graph, start, goal, manhattan_distance)
    euclidean_result = a_star(graph, start, goal, euclidean_distance)

    assert dijkstra_result.path_length == expected_length
    assert manhattan_result.path_length == expected_length
    assert euclidean_result.path_length == expected_length
    if expected_length is not None:
        for result in (dijkstra_result, manhattan_result, euclidean_result):
            assert_valid_path(graph, result.path, start, goal)


def test_a_star_visits_fewer_cells_than_dijkstra_on_open_grid():
    graph = GridGraph(20, 30)
    start, goal = (10, 3), (10, 26)

    dijkstra_result = dijkstra(graph, start, goal)
    a_star_result = a_star(graph, start, goal, manhattan_distance)

    assert a_star_result.path_length == dijkstra_result.path_length
    assert a_star_result.visited_count < dijkstra_result.visited_count


def test_more_informed_heuristic_visits_fewer_cells():
    graph, start, goal = parse_grid(MAP_WITH_MAZE)

    manhattan_result = a_star(graph, start, goal, manhattan_distance)
    euclidean_result = a_star(graph, start, goal, euclidean_distance)

    assert manhattan_result.visited_count <= euclidean_result.visited_count

