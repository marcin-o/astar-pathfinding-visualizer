import pygame

from algorithms.grid_graph import Cell
from visualization import theme
from visualization.animation import SearchAnimation
from visualization.board import Board


def cell_at(position: tuple[int, int]) -> Cell | None:
    if not theme.GRID_RECT.collidepoint(position):
        return None
    x, y = position
    return (y - theme.GRID_RECT.top) // theme.CELL_SIZE, (x - theme.GRID_RECT.left) // theme.CELL_SIZE


def cell_rect(cell: Cell) -> pygame.Rect:
    row, col = cell
    return pygame.Rect(
        theme.GRID_RECT.left + col * theme.CELL_SIZE + 1,
        theme.GRID_RECT.top + row * theme.CELL_SIZE + 1,
        theme.CELL_SIZE - 1,
        theme.CELL_SIZE - 1,
    )


def draw_grid(surface: pygame.Surface, fonts: theme.Fonts, board: Board, animation: SearchAnimation | None) -> None:
    surface.fill(theme.GRID_LINE, theme.GRID_RECT.inflate(2, 2))
    for cell in board.all_cells():
        surface.fill(theme.EMPTY, cell_rect(cell))
    if animation is not None:
        draw_search_state(surface, animation)
    for wall in board.walls:
        surface.fill(theme.WALL, cell_rect(wall))
    draw_endpoint(surface, fonts, board.start, theme.START, "S")
    draw_endpoint(surface, fonts, board.goal, theme.GOAL, "C")
    if animation is not None and animation.search_finished and not animation.result.path_found:
        draw_no_path_banner(surface, fonts)


def draw_search_state(surface: pygame.Surface, animation: SearchAnimation) -> None:
    for cell in animation.visit_times:
        surface.fill(visited_color(animation.visit_freshness(cell)), cell_rect(cell))
    for cell in animation.frontier:
        surface.fill(theme.FRONTIER, cell_rect(cell))
    if animation.current is not None:
        surface.fill(theme.CURRENT, cell_rect(animation.current))
    for cell in animation.visible_path:
        surface.fill(theme.PATH, cell_rect(cell))


def visited_color(freshness: float) -> pygame.Color:
    return pygame.Color(theme.VISITED).lerp(theme.VISITED_FRESH, freshness)


def draw_endpoint(surface: pygame.Surface, fonts: theme.Fonts, cell: Cell, color: tuple[int, int, int], label: str) -> None:
    rect = cell_rect(cell)
    surface.fill(color, rect)
    label_image = fonts.cell_label.render(label, True, theme.ENDPOINT_LABEL)
    surface.blit(label_image, label_image.get_rect(center=rect.center))


def draw_no_path_banner(surface: pygame.Surface, fonts: theme.Fonts) -> None:
    banner_rect = pygame.Rect(0, 0, theme.GRID_RECT.width, 96)
    banner_rect.center = theme.GRID_RECT.center
    banner = pygame.Surface(banner_rect.size, pygame.SRCALPHA)
    banner.fill((*theme.BACKGROUND, 225))
    surface.blit(banner, banner_rect)
    title = fonts.banner.render("BRAK ŚCIEŻKI", True, theme.DANGER)
    subtitle = fonts.body.render("Cel jest nieosiągalny z punktu startowego", True, theme.TEXT)
    surface.blit(title, title.get_rect(midbottom=(banner_rect.centerx, banner_rect.centery + 4)))
    surface.blit(subtitle, subtitle.get_rect(midtop=(banner_rect.centerx, banner_rect.centery + 8)))
