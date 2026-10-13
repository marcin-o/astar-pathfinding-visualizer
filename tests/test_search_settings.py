import random

from algorithms.heuristics import EUCLIDEAN, MANHATTAN
from visualization.board import Board
from visualization.search_settings import A_STAR, ALL_SETTINGS, DIJKSTRA, SearchSettings


def test_compared_variants_go_from_dijkstra_through_euclidean_to_manhattan():
    assert [settings.label for settings in ALL_SETTINGS] == ["Dijkstra", "A* · Euklidesowa", "A* · Manhattan"]


def test_heuristic_switching_alternates_between_manhattan_and_euclidean():
    settings = SearchSettings(A_STAR, MANHATTAN)

    assert settings.with_next_heuristic().heuristic_name == EUCLIDEAN
    assert settings.with_next_heuristic().with_next_heuristic().heuristic_name == MANHATTAN


def test_all_variants_find_equally_long_path_on_the_same_board():
    board = Board(27, 39)
    board.fill_with_maze(random.Random(5))

    results = [settings.run(board) for settings in ALL_SETTINGS]

    assert all(result.path_found for result in results)
    assert len({result.path_length for result in results}) == 1


def test_dijkstra_visits_most_cells_on_open_board():
    board = Board(27, 39)

    visited = {settings.label: settings.run(board).visited_count for settings in ALL_SETTINGS}

    assert visited[DIJKSTRA] > visited[f"A* · {EUCLIDEAN}"] >= visited[f"A* · {MANHATTAN}"]
