from dataclasses import dataclass

Cell = tuple[int, int]

MOVE_COST = 1
DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))


@dataclass(frozen=True)
class GridGraph:
    rows: int
    cols: int
    walls: frozenset[Cell] = frozenset()

    def contains(self, cell: Cell) -> bool:
        row, col = cell
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_walkable(self, cell: Cell) -> bool:
        return self.contains(cell) and cell not in self.walls

    def neighbors(self, cell: Cell) -> list[Cell]:
        row, col = cell
        candidates = [(row + d_row, col + d_col) for d_row, d_col in DIRECTIONS]
        return [candidate for candidate in candidates if self.is_walkable(candidate)]
