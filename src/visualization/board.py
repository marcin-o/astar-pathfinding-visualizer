import random

from algorithms.grid_graph import Cell, GridGraph

RANDOM_WALL_DENSITY = 0.3
MAZE_EXTRA_OPENING_CHANCE = 0.12


class Board:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.walls: set[Cell] = set()
        self.start, self.goal = self.default_endpoints()

    def default_endpoints(self) -> tuple[Cell, Cell]:
        middle_row = self.rows // 2
        return (middle_row, self.cols // 6), (middle_row, self.cols - 1 - self.cols // 6)

    def contains(self, cell: Cell) -> bool:
        row, col = cell
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_endpoint(self, cell: Cell) -> bool:
        return cell in (self.start, self.goal)

    def add_walls(self, cells: list[Cell]) -> bool:
        new_walls = {cell for cell in cells if self.contains(cell) and not self.is_endpoint(cell)} - self.walls
        self.walls |= new_walls
        return bool(new_walls)

    def remove_walls(self, cells: list[Cell]) -> bool:
        removed_walls = self.walls & set(cells)
        self.walls -= removed_walls
        return bool(removed_walls)

    def move_start(self, cell: Cell) -> bool:
        if not self.can_place_endpoint(cell):
            return False
        self.start = cell
        return True

    def move_goal(self, cell: Cell) -> bool:
        if not self.can_place_endpoint(cell):
            return False
        self.goal = cell
        return True

    def can_place_endpoint(self, cell: Cell) -> bool:
        return self.contains(cell) and cell not in self.walls and not self.is_endpoint(cell)

    def clear(self) -> None:
        self.walls.clear()
        self.start, self.goal = self.default_endpoints()

    def fill_with_random_walls(self, rng: random.Random) -> None:
        self.walls = {
            cell
            for cell in self.all_cells()
            if rng.random() < RANDOM_WALL_DENSITY and not self.is_endpoint(cell)
        }

    def fill_with_maze(self, rng: random.Random) -> None:
        passages = {(row, col) for row in range(1, self.rows - 1, 2) for col in range(1, self.cols - 1, 2)}
        self.walls = set(self.all_cells()) - passages
        self.carve_maze(passages, rng)
        self.open_extra_shortcuts(rng)
        self.start, self.goal = min(passages), max(passages)

    def carve_maze(self, passages: set[Cell], rng: random.Random) -> None:
        first = rng.choice(sorted(passages))
        reached = {first}
        stack = [first]
        while stack:
            row, col = stack[-1]
            candidates = [
                (row + d_row, col + d_col)
                for d_row, d_col in ((-2, 0), (2, 0), (0, -2), (0, 2))
                if (row + d_row, col + d_col) in passages - reached
            ]
            if not candidates:
                stack.pop()
                continue
            next_row, next_col = rng.choice(candidates)
            self.walls.discard(((row + next_row) // 2, (col + next_col) // 2))
            reached.add((next_row, next_col))
            stack.append((next_row, next_col))

    def open_extra_shortcuts(self, rng: random.Random) -> None:
        inner_walls_between_passages = [
            (row, col)
            for row, col in sorted(self.walls)
            if 0 < row < self.rows - 1 and 0 < col < self.cols - 1 and (row % 2) != (col % 2)
        ]
        for wall in inner_walls_between_passages:
            if rng.random() < MAZE_EXTRA_OPENING_CHANCE:
                self.walls.discard(wall)

    def all_cells(self) -> list[Cell]:
        return [(row, col) for row in range(self.rows) for col in range(self.cols)]

    def to_graph(self) -> GridGraph:
        return GridGraph(self.rows, self.cols, frozenset(self.walls))
