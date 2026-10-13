from collections import deque

from algorithms.grid_graph import Cell, GridGraph


def parse_grid(text: str) -> tuple[GridGraph, Cell, Cell]:
    lines = [line.strip() for line in text.strip().splitlines()]
    symbols = {(row, col): symbol for row, line in enumerate(lines) for col, symbol in enumerate(line)}
    walls = frozenset(cell for cell, symbol in symbols.items() if symbol == "#")
    start = next(cell for cell, symbol in symbols.items() if symbol == "S")
    goal = next(cell for cell, symbol in symbols.items() if symbol == "G")
    return GridGraph(len(lines), len(lines[0]), walls), start, goal


def breadth_first_distances(graph: GridGraph, source: Cell) -> dict[Cell, int]:
    distances = {source: 0}
    queue = deque([source])
    while queue:
        current = queue.popleft()
        for neighbor in graph.neighbors(current):
            if neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)
    return distances


def assert_valid_path(graph: GridGraph, path: list[Cell], start: Cell, goal: Cell) -> None:
    assert path[0] == start
    assert path[-1] == goal
    assert all(graph.is_walkable(cell) for cell in path)
    for previous, current in zip(path, path[1:]):
        assert abs(previous[0] - current[0]) + abs(previous[1] - current[1]) == 1
