from algorithms.dijkstra import dijkstra
from algorithms.grid_graph import GridGraph
from visualization.animation import SearchAnimation


def open_grid_animation() -> SearchAnimation:
    return SearchAnimation(dijkstra(GridGraph(8, 8), (0, 0), (7, 7)))


def test_advance_applies_steps_proportionally_to_elapsed_time():
    animation = open_grid_animation()

    animation.advance(0.5, steps_per_second=10)

    assert animation.applied_steps == 5
    assert len(animation.visit_times) == 5


def test_paused_animation_does_not_progress():
    animation = open_grid_animation()
    animation.toggle_pause()

    animation.advance(1.0, steps_per_second=10)

    assert animation.applied_steps == 0


def test_frontier_never_contains_visited_cells():
    animation = open_grid_animation()

    while not animation.search_finished:
        animation.advance(0.1, steps_per_second=10)
        assert not animation.frontier & animation.visit_times.keys()


def test_path_is_revealed_only_after_search_finishes():
    animation = open_grid_animation()

    animation.advance(0.5, steps_per_second=10)
    assert animation.visible_path == []

    animation.skip_to_end()
    assert animation.finished
    assert animation.visible_path == animation.result.path
    assert animation.current is None
