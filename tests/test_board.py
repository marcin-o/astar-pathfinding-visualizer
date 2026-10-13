import random

import pytest

from algorithms.dijkstra import dijkstra
from visualization.board import Board


def test_walls_are_never_placed_on_start_or_goal():
    board = Board(10, 12)

    board.add_walls([board.start, board.goal, (0, 0)])

    assert board.walls == {(0, 0)}


def test_endpoints_cannot_be_moved_onto_walls_or_each_other():
    board = Board(10, 12)
    board.add_walls([(0, 0)])
    original_start = board.start

    assert not board.move_start((0, 0))
    assert not board.move_start(board.goal)
    assert not board.move_goal((20, 20))
    assert board.start == original_start


def test_moving_start_to_free_cell_succeeds():
    board = Board(10, 12)

    assert board.move_start((1, 1))
    assert board.start == (1, 1)


def test_removing_walls_reports_whether_board_changed():
    board = Board(10, 12)
    board.add_walls([(0, 0), (0, 1)])

    assert board.remove_walls([(0, 0)])
    assert not board.remove_walls([(0, 0)])
    assert board.walls == {(0, 1)}


def test_clear_removes_walls_and_restores_endpoints():
    board = Board(10, 12)
    default_endpoints = (board.start, board.goal)
    board.move_start((0, 0))
    board.add_walls([(5, 5)])

    board.clear()

    assert board.walls == set()
    assert (board.start, board.goal) == default_endpoints


def test_random_walls_keep_endpoints_free():
    board = Board(27, 39)

    board.fill_with_random_walls(random.Random(1))

    assert board.walls
    assert board.start not in board.walls
    assert board.goal not in board.walls


@pytest.mark.parametrize("seed", range(10))
def test_maze_always_connects_start_with_goal(seed):
    board = Board(27, 39)

    board.fill_with_maze(random.Random(seed))

    assert board.start not in board.walls
    assert board.goal not in board.walls
    assert dijkstra(board.to_graph(), board.start, board.goal).path_found
