from dataclasses import dataclass

from algorithms.grid_graph import Cell


@dataclass(frozen=True)
class ExplorationStep:
    current: Cell
    discovered: tuple[Cell, ...]


@dataclass(frozen=True)
class SearchResult:
    path: list[Cell]
    steps: list[ExplorationStep]

    @property
    def path_found(self) -> bool:
        return bool(self.path)

    @property
    def path_length(self) -> int | None:
        return len(self.path) - 1 if self.path else None

    @property
    def visited_count(self) -> int:
        return len(self.steps)


def reconstruct_path(came_from: dict[Cell, Cell], start: Cell, goal: Cell) -> list[Cell]:
    path = [goal]
    while path[-1] != start:
        path.append(came_from[path[-1]])
    path.reverse()
    return path
