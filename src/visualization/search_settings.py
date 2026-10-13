from dataclasses import dataclass

from algorithms.astar import a_star
from algorithms.dijkstra import dijkstra
from algorithms.heuristics import ADMISSIBLE_HEURISTICS, HEURISTICS
from algorithms.search_result import SearchResult
from visualization.board import Board

A_STAR = "A*"
DIJKSTRA = "Dijkstra"
HEURISTIC_NAMES = tuple(HEURISTICS)


@dataclass(frozen=True)
class SearchSettings:
    algorithm: str = A_STAR
    heuristic_name: str = HEURISTIC_NAMES[0]

    @property
    def uses_heuristic(self) -> bool:
        return self.algorithm == A_STAR

    @property
    def heuristic_is_admissible(self) -> bool:
        return self.heuristic_name in ADMISSIBLE_HEURISTICS

    @property
    def label(self) -> str:
        return f"A* · {self.heuristic_name}" if self.uses_heuristic else DIJKSTRA

    def with_algorithm(self, algorithm: str) -> "SearchSettings":
        return SearchSettings(algorithm, self.heuristic_name)

    def with_next_heuristic(self) -> "SearchSettings":
        next_index = (HEURISTIC_NAMES.index(self.heuristic_name) + 1) % len(HEURISTIC_NAMES)
        return SearchSettings(self.algorithm, HEURISTIC_NAMES[next_index])

    def run(self, board: Board) -> SearchResult:
        graph = board.to_graph()
        if self.uses_heuristic:
            return a_star(graph, board.start, board.goal, HEURISTICS[self.heuristic_name])
        return dijkstra(graph, board.start, board.goal)


ALL_SETTINGS = tuple(SearchSettings(A_STAR, name) for name in HEURISTIC_NAMES) + (SearchSettings(DIJKSTRA),)
