from algorithms.grid_graph import GridGraph


def test_inner_cell_has_four_neighbors_without_diagonals():
    graph = GridGraph(3, 3)

    assert sorted(graph.neighbors((1, 1))) == [(0, 1), (1, 0), (1, 2), (2, 1)]


def test_corner_cell_has_only_neighbors_inside_grid():
    graph = GridGraph(3, 3)

    assert sorted(graph.neighbors((0, 0))) == [(0, 1), (1, 0)]


def test_walls_are_not_neighbors():
    graph = GridGraph(3, 3, frozenset({(0, 1), (1, 2)}))

    assert sorted(graph.neighbors((1, 1))) == [(1, 0), (2, 1)]


def test_walkability_respects_bounds_and_walls():
    graph = GridGraph(2, 2, frozenset({(1, 1)}))

    assert graph.is_walkable((0, 0))
    assert not graph.is_walkable((1, 1))
    assert not graph.is_walkable((-1, 0))
    assert not graph.is_walkable((0, 2))
