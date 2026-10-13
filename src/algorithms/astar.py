import heapq
import math

from algorithms.grid_graph import MOVE_COST, Cell, GridGraph
from algorithms.heuristics import Heuristic
from algorithms.search_result import ExplorationStep, SearchResult, reconstruct_path


def a_star(graph: GridGraph, start: Cell, goal: Cell, heuristic: Heuristic) -> SearchResult:
    g_score: dict[Cell, float] = {start: 0}
    came_from: dict[Cell, Cell] = {}
    start_h = heuristic(start, goal)
    open_queue = [(start_h, start_h, start)]
    closed: set[Cell] = set()
    steps: list[ExplorationStep] = []

    while open_queue:
        _, _, current = heapq.heappop(open_queue)
        if current in closed:
            continue
        closed.add(current)

        if current == goal:
            steps.append(ExplorationStep(current, ()))
            return SearchResult(reconstruct_path(came_from, start, goal), steps)

        discovered = []
        for neighbor in graph.neighbors(current):
            if neighbor in closed:
                continue
            tentative_g = g_score[current] + MOVE_COST
            if tentative_g < g_score.get(neighbor, math.inf):
                g_score[neighbor] = tentative_g
                came_from[neighbor] = current
                h = heuristic(neighbor, goal)
                f = tentative_g + h
                heapq.heappush(open_queue, (f, h, neighbor))
                discovered.append(neighbor)
        steps.append(ExplorationStep(current, tuple(discovered)))

    return SearchResult([], steps)
