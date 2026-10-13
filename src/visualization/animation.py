from algorithms.grid_graph import Cell
from algorithms.search_result import SearchResult

PATH_CELLS_PER_SECOND = 45
VISIT_HIGHLIGHT_SECONDS = 0.45


class SearchAnimation:
    def __init__(self, result: SearchResult):
        self.result = result
        self.applied_steps = 0
        self.revealed_path_cells = 0
        self.visit_times: dict[Cell, float] = {}
        self.frontier: set[Cell] = set()
        self.current: Cell | None = None
        self.paused = False
        self.elapsed = 0.0
        self.step_budget = 0.0
        self.path_budget = 0.0

    @property
    def search_finished(self) -> bool:
        return self.applied_steps == len(self.result.steps)

    @property
    def finished(self) -> bool:
        return self.search_finished and self.revealed_path_cells == len(self.result.path)

    @property
    def visible_path(self) -> list[Cell]:
        return self.result.path[: self.revealed_path_cells]

    def advance(self, seconds: float, steps_per_second: float) -> None:
        if self.paused:
            return
        self.elapsed += seconds
        if not self.search_finished:
            self.step_budget += seconds * steps_per_second
            while self.step_budget >= 1 and not self.search_finished:
                self.step_budget -= 1
                self.apply_next_step(self.elapsed)
        elif not self.finished:
            self.path_budget += seconds * PATH_CELLS_PER_SECOND
            revealed = self.revealed_path_cells + int(self.path_budget)
            self.path_budget -= int(self.path_budget)
            self.revealed_path_cells = min(revealed, len(self.result.path))

    def skip_to_end(self) -> None:
        already_faded = self.elapsed - VISIT_HIGHLIGHT_SECONDS
        while not self.search_finished:
            self.apply_next_step(already_faded)
        self.revealed_path_cells = len(self.result.path)
        self.paused = False

    def toggle_pause(self) -> None:
        self.paused = not self.paused

    def apply_next_step(self, visit_time: float) -> None:
        step = self.result.steps[self.applied_steps]
        self.applied_steps += 1
        self.visit_times[step.current] = visit_time
        self.frontier.discard(step.current)
        self.frontier.update(cell for cell in step.discovered if cell not in self.visit_times)
        self.current = None if self.search_finished else step.current

    def visit_freshness(self, cell: Cell) -> float:
        age = self.elapsed - self.visit_times[cell]
        return max(0.0, 1.0 - age / VISIT_HIGHLIGHT_SECONDS)
