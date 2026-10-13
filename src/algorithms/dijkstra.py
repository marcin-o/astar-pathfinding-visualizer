import heapq
import math

from algorithms.grid_graph import MOVE_COST, Cell, GridGraph
from algorithms.search_result import ExplorationStep, SearchResult, reconstruct_path


def dijkstra(graph: GridGraph, start: Cell, goal: Cell) -> SearchResult:
    distance: dict[Cell, float] = {start: 0}
    came_from: dict[Cell, Cell] = {}
    queue = [(0, start)]
    visited: set[Cell] = set()
    steps: list[ExplorationStep] = []

    while queue:
        current_distance, current = heapq.heappop(queue)
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            steps.append(ExplorationStep(current, ()))
            return SearchResult(reconstruct_path(came_from, start, goal), steps)

        discovered = []
        for neighbor in graph.neighbors(current):
            if neighbor in visited:
                continue
            new_distance = current_distance + MOVE_COST
            if new_distance < distance.get(neighbor, math.inf):
                distance[neighbor] = new_distance
                came_from[neighbor] = current
                heapq.heappush(queue, (new_distance, neighbor))
                discovered.append(neighbor)
        steps.append(ExplorationStep(current, tuple(discovered)))

    return SearchResult([], steps)
