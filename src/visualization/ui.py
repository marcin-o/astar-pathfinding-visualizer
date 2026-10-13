import pygame

from algorithms.heuristics import EUCLIDEAN, MANHATTAN
from algorithms.search_result import SearchResult
from visualization import theme
from visualization.animation import SearchAnimation
from visualization.search_settings import ALL_SETTINGS, SearchSettings

PADDING = 16
ROW_HEIGHT = 26
NOTE_HEIGHT = 21
TABLE_ROW_HEIGHT = 24

HEURISTIC_FORMULAS = {
    MANHATTAN: "h(n) = |Δx| + |Δy|",
    EUCLIDEAN: "h(n) = √(Δx² + Δy²)",
}

LEGEND_ITEMS = (
    (theme.START, "Start (S)"),
    (theme.GOAL, "Cel (C)"),
    (theme.WALL, "Przeszkoda"),
    (theme.EMPTY, "Puste pole"),
    (theme.CURRENT, "Analizowane"),
    (theme.VISITED, "Odwiedzone"),
    (theme.FRONTIER, "Kandydaci"),
    (theme.PATH, "Ścieżka"),
)

CONTROL_COLUMNS = (
    (("LPM", "rysuj przeszkody"), ("LPM na S / C", "przeciągnij"), ("PPM", "usuń przeszkody"), ("Esc", "wyjście")),
    (("Spacja", "start / pauza"), ("Enter", "pomiń animację"), ("A / D", "A* / Dijkstra"), ("H", "zmień heurystykę")),
    (("P", "porównaj warianty"), ("+ / −", "prędkość"), ("C", "wyczyść wynik"), ("R", "wyczyść planszę")),
    (("L", "losowe przeszkody"), ("M", "labirynt"), ("F", "pełny ekran")),
)
CONTROLS_PADDING = 14
CONTROLS_KEY_GAP = 8


class PanelWriter:
    def __init__(self, surface: pygame.Surface, fonts: theme.Fonts, rect: pygame.Rect):
        self.surface = surface
        self.fonts = fonts
        self.left = rect.left + PADDING
        self.right = rect.right - PADDING
        self.y = rect.top + PADDING

    def text(self, font: pygame.font.Font, text: str, color, **anchor) -> None:
        image = font.render(text, True, color)
        self.surface.blit(image, image.get_rect(**anchor))

    def title(self, text: str, subtitle: str) -> None:
        self.text(self.fonts.title, text, theme.TEXT, topleft=(self.left, self.y))
        self.text(self.fonts.small, subtitle, theme.MUTED_TEXT, topleft=(self.left, self.y + 34))
        self.y += 58

    def heading(self, text: str) -> None:
        self.y += 10
        self.text(self.fonts.heading, text, theme.HEADING, topleft=(self.left, self.y))
        self.y += 24

    def row(self, label: str, value: str, value_color=theme.TEXT) -> None:
        self.text(self.fonts.body, label, theme.MUTED_TEXT, topleft=(self.left, self.y))
        self.text(self.fonts.body_bold, value, value_color, topright=(self.right, self.y))
        self.y += ROW_HEIGHT

    def note(self, text: str) -> None:
        self.text(self.fonts.small, text, theme.MUTED_TEXT, topright=(self.right, self.y))
        self.y += NOTE_HEIGHT

    def status(self, text: str, color) -> None:
        self.text(self.fonts.body_bold, text, color, topleft=(self.left, self.y))
        self.y += ROW_HEIGHT + 4


def draw_panel(
    surface: pygame.Surface,
    fonts: theme.Fonts,
    settings: SearchSettings,
    steps_per_second: int,
    animation: SearchAnimation | None,
    comparison: dict[str, SearchResult],
) -> None:
    pygame.draw.rect(surface, theme.PANEL_BACKGROUND, theme.PANEL_RECT, border_radius=10)
    writer = PanelWriter(surface, fonts, theme.PANEL_RECT)
    writer.title("A* Pathfinding Visualizer", "Grafy i ich zastosowania")
    draw_settings_section(writer, settings, steps_per_second)
    draw_result_section(writer, animation)
    draw_comparison_section(writer, comparison)
    draw_legend_section(writer)


def draw_settings_section(writer: PanelWriter, settings: SearchSettings, steps_per_second: int) -> None:
    writer.heading("USTAWIENIA")
    writer.row("Algorytm", settings.algorithm)
    if settings.uses_heuristic:
        writer.note("f(n) = g(n) + h(n)")
        writer.row("Heurystyka", settings.heuristic_name)
        writer.note(HEURISTIC_FORMULAS[settings.heuristic_name])
    else:
        writer.note("f(n) = g(n)")
        writer.row("Heurystyka", "brak", theme.MUTED_TEXT)
        writer.note("h(n) = 0")
    writer.row("Prędkość", f"{steps_per_second} kroków/s")


def draw_result_section(writer: PanelWriter, animation: SearchAnimation | None) -> None:
    writer.heading("WYNIK")
    status_text, status_color = describe_status(animation)
    writer.status(status_text, status_color)
    if animation is None:
        writer.row("Odwiedzone wierzchołki", "–")
        writer.row("Kandydaci w kolejce", "–")
        writer.row("Długość ścieżki", "–")
        return
    writer.row("Odwiedzone wierzchołki", str(animation.applied_steps))
    writer.row("Kandydaci w kolejce", str(len(animation.frontier)))
    writer.row("Długość ścieżki", describe_path_length(animation))


def describe_status(animation: SearchAnimation | None) -> tuple[str, tuple[int, int, int]]:
    if animation is None:
        return "Gotowy – naciśnij Spację", theme.MUTED_TEXT
    if animation.paused:
        return "Pauza", theme.HEADING
    if not animation.search_finished:
        return "Wyszukiwanie…", theme.TEXT
    if animation.result.path_found:
        return "Znaleziono ścieżkę", theme.SUCCESS
    return "Brak ścieżki do celu!", theme.DANGER


def describe_path_length(animation: SearchAnimation) -> str:
    if not animation.search_finished:
        return "…"
    if not animation.result.path_found:
        return "brak"
    return str(animation.result.path_length)


def draw_comparison_section(writer: PanelWriter, comparison: dict[str, SearchResult]) -> None:
    writer.heading("PORÓWNANIE (ta sama plansza)")
    visited_column = writer.right - 80
    writer.text(writer.fonts.small, "wariant", theme.MUTED_TEXT, topleft=(writer.left, writer.y))
    writer.text(writer.fonts.small, "odwiedzone", theme.MUTED_TEXT, topright=(visited_column, writer.y))
    writer.text(writer.fonts.small, "ścieżka", theme.MUTED_TEXT, topright=(writer.right, writer.y))
    writer.y += NOTE_HEIGHT
    table_top = writer.y

    compared = [(settings.label, comparison[settings.label]) for settings in ALL_SETTINGS if settings.label in comparison]
    if not compared:
        writer.text(writer.fonts.small, "Uruchom kilka wariantów lub naciśnij P", theme.MUTED_TEXT, topleft=(writer.left, writer.y))
    for label, result in compared:
        path_text = str(result.path_length) if result.path_found else "brak"
        writer.text(writer.fonts.body, label, theme.TEXT, topleft=(writer.left, writer.y))
        writer.text(writer.fonts.body_bold, str(result.visited_count), theme.TEXT, topright=(visited_column, writer.y))
        writer.text(writer.fonts.body_bold, path_text, theme.TEXT, topright=(writer.right, writer.y))
        writer.y += TABLE_ROW_HEIGHT
    writer.y = table_top + len(ALL_SETTINGS) * TABLE_ROW_HEIGHT


def draw_legend_section(writer: PanelWriter) -> None:
    writer.heading("LEGENDA")
    column_width = (writer.right - writer.left) // 2
    for index, (color, label) in enumerate(LEGEND_ITEMS):
        x = writer.left + (index % 2) * column_width
        y = writer.y + (index // 2) * ROW_HEIGHT
        swatch = pygame.Rect(x, y + 3, 18, 18)
        writer.surface.fill(color, swatch)
        pygame.draw.rect(writer.surface, theme.GRID_LINE, swatch, width=1)
        writer.text(writer.fonts.body, label, theme.TEXT, topleft=(x + 28, y))
    writer.y += (len(LEGEND_ITEMS) + 1) // 2 * ROW_HEIGHT


def draw_controls(surface: pygame.Surface, fonts: theme.Fonts) -> None:
    pygame.draw.rect(surface, theme.PANEL_BACKGROUND, theme.CONTROLS_RECT, border_radius=10)
    rendered_columns = [
        [(fonts.small_bold.render(key, True, theme.HEADING), fonts.small.render(action, True, theme.TEXT)) for key, action in column]
        for column in CONTROL_COLUMNS
    ]
    key_widths = [max(key.get_width() for key, _ in column) + CONTROLS_KEY_GAP for column in rendered_columns]
    column_widths = [
        key_width + max(action.get_width() for _, action in column)
        for key_width, column in zip(key_widths, rendered_columns)
    ]
    free_width = theme.CONTROLS_RECT.width - 2 * CONTROLS_PADDING - sum(column_widths)
    column_gap = free_width / (len(rendered_columns) - 1)
    line_height = (theme.CONTROLS_RECT.height - 8) // max(len(column) for column in CONTROL_COLUMNS)

    x = theme.CONTROLS_RECT.left + CONTROLS_PADDING
    for column, key_width, column_width in zip(rendered_columns, key_widths, column_widths):
        for row_index, (key_image, action_image) in enumerate(column):
            y = theme.CONTROLS_RECT.top + 4 + row_index * line_height
            surface.blit(key_image, (x, y))
            surface.blit(action_image, (x + key_width, y))
        x += column_width + column_gap
