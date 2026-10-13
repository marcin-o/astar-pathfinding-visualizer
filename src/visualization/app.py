import os
import random
from enum import Enum, auto

import pygame

from algorithms.grid_graph import Cell
from algorithms.search_result import SearchResult
from visualization import theme
from visualization.animation import SearchAnimation
from visualization.board import Board
from visualization.grid import cell_at, draw_grid
from visualization.search_settings import A_STAR, ALL_SETTINGS, DIJKSTRA, SearchSettings
from visualization.ui import draw_controls, draw_panel

LEFT_BUTTON = 1
RIGHT_BUTTON = 3


class DragMode(Enum):
    DRAW_WALLS = auto()
    ERASE_WALLS = auto()
    MOVE_START = auto()
    MOVE_GOAL = auto()


class App:
    def __init__(self):
        os.environ.setdefault("SDL_RENDER_SCALE_QUALITY", "linear")
        pygame.init()
        self.screen = pygame.display.set_mode(theme.WINDOW_SIZE, pygame.SCALED | pygame.RESIZABLE)
        pygame.display.set_caption("A* Pathfinding Visualizer")
        self.fonts = theme.load_fonts()
        self.clock = pygame.time.Clock()
        self.rng = random.Random()
        self.board = Board(theme.GRID_ROWS, theme.GRID_COLS)
        self.settings = SearchSettings()
        self.speed_index = theme.DEFAULT_SPEED_INDEX
        self.animation: SearchAnimation | None = None
        self.comparison: dict[str, SearchResult] = {}
        self.drag_mode: DragMode | None = None
        self.last_drag_cell: Cell | None = None
        self.fullscreen = False
        self.running = True
        self.key_actions = {
            pygame.K_SPACE: self.start_or_pause,
            pygame.K_RETURN: self.skip_animation,
            pygame.K_KP_ENTER: self.skip_animation,
            pygame.K_a: lambda: self.change_settings(self.settings.with_algorithm(A_STAR)),
            pygame.K_d: lambda: self.change_settings(self.settings.with_algorithm(DIJKSTRA)),
            pygame.K_h: self.select_next_heuristic,
            pygame.K_EQUALS: self.speed_up,
            pygame.K_PLUS: self.speed_up,
            pygame.K_KP_PLUS: self.speed_up,
            pygame.K_UP: self.speed_up,
            pygame.K_MINUS: self.slow_down,
            pygame.K_KP_MINUS: self.slow_down,
            pygame.K_DOWN: self.slow_down,
            pygame.K_p: self.compare_all,
            pygame.K_c: self.clear_result,
            pygame.K_r: lambda: self.rebuild_board(self.board.clear),
            pygame.K_l: lambda: self.rebuild_board(lambda: self.board.fill_with_random_walls(self.rng)),
            pygame.K_m: lambda: self.rebuild_board(lambda: self.board.fill_with_maze(self.rng)),
            pygame.K_f: self.toggle_fullscreen,
            pygame.K_F11: self.toggle_fullscreen,
            pygame.K_ESCAPE: self.leave_fullscreen_or_quit,
        }

    @property
    def steps_per_second(self) -> int:
        return theme.SPEED_LEVELS[self.speed_index]

    def run(self) -> None:
        while self.running:
            seconds = self.clock.tick(theme.FPS) / 1000
            for event in pygame.event.get():
                self.handle_event(event)
            self.update(seconds)
            self.draw()
        pygame.quit()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN and event.key in self.key_actions:
            self.key_actions[event.key]()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.start_drag(event.button, event.pos)
        elif event.type == pygame.MOUSEMOTION:
            self.continue_drag(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.drag_mode = None

    def update(self, seconds: float) -> None:
        if self.animation is None:
            return
        self.animation.advance(seconds, self.steps_per_second)
        if self.animation.search_finished:
            self.comparison[self.settings.label] = self.animation.result

    def draw(self) -> None:
        self.screen.fill(theme.BACKGROUND)
        draw_grid(self.screen, self.fonts, self.board, self.animation)
        draw_panel(self.screen, self.fonts, self.settings, self.steps_per_second, self.animation, self.comparison)
        draw_controls(self.screen, self.fonts)
        pygame.display.flip()

    def start_or_pause(self) -> None:
        if self.animation is None or self.animation.finished:
            self.animation = SearchAnimation(self.settings.run(self.board))
        else:
            self.animation.toggle_pause()

    def skip_animation(self) -> None:
        if self.animation is not None:
            self.animation.skip_to_end()

    def show_result_instantly(self) -> None:
        self.animation = SearchAnimation(self.settings.run(self.board))
        self.animation.skip_to_end()

    def clear_result(self) -> None:
        self.animation = None

    def change_settings(self, settings: SearchSettings) -> None:
        if settings != self.settings:
            self.settings = settings
            self.clear_result()

    def select_next_heuristic(self) -> None:
        if self.settings.uses_heuristic:
            self.change_settings(self.settings.with_next_heuristic())
        else:
            self.change_settings(self.settings.with_algorithm(A_STAR))

    def speed_up(self) -> None:
        self.speed_index = min(self.speed_index + 1, len(theme.SPEED_LEVELS) - 1)

    def slow_down(self) -> None:
        self.speed_index = max(self.speed_index - 1, 0)

    def compare_all(self) -> None:
        for settings in ALL_SETTINGS:
            self.comparison[settings.label] = settings.run(self.board)

    def rebuild_board(self, rebuild) -> None:
        rebuild()
        self.comparison.clear()
        self.clear_result()

    def on_board_edited(self) -> None:
        self.comparison.clear()
        if self.animation is not None:
            self.show_result_instantly()

    def start_drag(self, button: int, position: tuple[int, int]) -> None:
        cell = cell_at(position)
        if cell is None:
            return
        if button == LEFT_BUTTON:
            self.drag_mode = self.left_drag_mode_for(cell)
        elif button == RIGHT_BUTTON:
            self.drag_mode = DragMode.ERASE_WALLS
        else:
            return
        self.last_drag_cell = cell
        self.apply_drag(cell)

    def left_drag_mode_for(self, cell: Cell) -> DragMode:
        if cell == self.board.start:
            return DragMode.MOVE_START
        if cell == self.board.goal:
            return DragMode.MOVE_GOAL
        return DragMode.DRAW_WALLS

    def continue_drag(self, position: tuple[int, int]) -> None:
        cell = cell_at(position)
        if self.drag_mode is not None and cell is not None and cell != self.last_drag_cell:
            self.apply_drag(cell)

    def apply_drag(self, cell: Cell) -> None:
        stroke = cells_on_line(self.last_drag_cell, cell)
        self.last_drag_cell = cell
        if self.drag_mode == DragMode.DRAW_WALLS:
            board_changed = self.board.add_walls(stroke)
        elif self.drag_mode == DragMode.ERASE_WALLS:
            board_changed = self.board.remove_walls(stroke)
        elif self.drag_mode == DragMode.MOVE_START:
            board_changed = self.board.move_start(cell)
        else:
            board_changed = self.board.move_goal(cell)
        if board_changed:
            self.on_board_edited()

    def toggle_fullscreen(self) -> None:
        pygame.display.toggle_fullscreen()
        self.fullscreen = not self.fullscreen

    def leave_fullscreen_or_quit(self) -> None:
        if self.fullscreen:
            self.toggle_fullscreen()
        else:
            self.running = False


def cells_on_line(start: Cell, end: Cell) -> list[Cell]:
    row_delta = end[0] - start[0]
    col_delta = end[1] - start[1]
    steps = max(abs(row_delta), abs(col_delta), 1)
    return [
        (round(start[0] + row_delta * step / steps), round(start[1] + col_delta * step / steps))
        for step in range(steps + 1)
    ]
