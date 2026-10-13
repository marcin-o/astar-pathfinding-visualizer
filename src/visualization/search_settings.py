from dataclasses import dataclass

from algorithms.astar import a_star
from algorithms.dijkstra import dijkstra
from algorithms.heuristics import EUCLIDEAN, HEURISTICS, MANHATTAN
from algorithms.search_result import SearchResult
from visualization.board import Board

A_STAR = "A*"
DIJKSTRA = "Dijkstra"
HEURISTIC_NAMES = tuple(HEURISTICS)


@dataclass(frozen=True)
class SearchSettings:
    algorithm: str = A_STAR
    heuristic_name: str = MANHATTAN

    @property
    def uses_heuristic(self) -> bool:
        return self.algorithm == A_STAR

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


ALL_SETTINGS = (
    SearchSettings(DIJKSTRA),
    SearchSettings(A_STAR, EUCLIDEAN),
    SearchSettings(A_STAR, MANHATTAN),
)
