from dataclasses import dataclass

import pygame

WINDOW_SIZE = (1280, 720)
FPS = 60
MARGIN = 16

GRID_ROWS = 27
GRID_COLS = 39
CELL_SIZE = 22
GRID_RECT = pygame.Rect(MARGIN, MARGIN, GRID_COLS * CELL_SIZE, GRID_ROWS * CELL_SIZE)
CONTROLS_RECT = pygame.Rect(MARGIN, GRID_RECT.bottom + 12, GRID_RECT.width, WINDOW_SIZE[1] - GRID_RECT.bottom - 12 - MARGIN)
PANEL_RECT = pygame.Rect(GRID_RECT.right + 20, MARGIN, WINDOW_SIZE[0] - GRID_RECT.right - 20 - MARGIN, WINDOW_SIZE[1] - 2 * MARGIN)

SPEED_LEVELS = (5, 15, 40, 100, 250, 600, 1500)
DEFAULT_SPEED_INDEX = 3

BACKGROUND = (22, 26, 36)
PANEL_BACKGROUND = (33, 38, 52)
TEXT = (236, 239, 244)
MUTED_TEXT = (150, 160, 182)
HEADING = (255, 200, 70)
SUCCESS = (90, 215, 140)
DANGER = (255, 105, 105)

GRID_LINE = (200, 206, 218)
EMPTY = (248, 249, 251)
WALL = (42, 46, 60)
START = (34, 170, 90)
GOAL = (226, 64, 64)
VISITED = (150, 185, 245)
VISITED_FRESH = (60, 100, 225)
FRONTIER = (165, 235, 190)
CURRENT = (255, 125, 40)
PATH = (255, 205, 40)
ENDPOINT_LABEL = (255, 255, 255)

REGULAR_FONT_NAMES = "segoeuisemibold,dejavusans,helvetica"
BOLD_FONT_NAMES = "segoeui,dejavusans,helvetica"


@dataclass(frozen=True)
class Fonts:
    title: pygame.font.Font
    heading: pygame.font.Font
    body: pygame.font.Font
    body_bold: pygame.font.Font
    small: pygame.font.Font
    small_bold: pygame.font.Font
    cell_label: pygame.font.Font
    banner: pygame.font.Font


def regular_font(size: int) -> pygame.font.Font:
    return pygame.font.SysFont(REGULAR_FONT_NAMES, size)


def bold_font(size: int) -> pygame.font.Font:
    return pygame.font.SysFont(BOLD_FONT_NAMES, size, bold=True)


def load_fonts() -> Fonts:
    return Fonts(
        title=bold_font(26),
        heading=bold_font(16),
        body=regular_font(19),
        body_bold=bold_font(19),
        small=regular_font(16),
        small_bold=bold_font(16),
        cell_label=bold_font(15),
        banner=bold_font(30),
    )
