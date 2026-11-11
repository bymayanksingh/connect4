import pygame

from connect4.game import Connect4Game
from connect4.gui.assets import assets
from connect4.gui.renderer import GameRenderer
from connect4.types import GameMode


def test_asset_manager_surface_generation():
    # Verify fallback procedural surface generation works headlessly
    surf = assets.get_coin_surface((255, 0, 0), radius=30)
    assert isinstance(surf, pygame.Surface)
    assert surf.get_width() == 60
    assert surf.get_height() == 60


def test_headless_game_renderer_draw():
    pygame.init()
    screen = pygame.display.set_mode((700, 700))
    game = Connect4Game(mode=GameMode.PVP)
    renderer = GameRenderer(screen=screen, sq_size=100)

    # Drawing on headless surface should succeed with zero errors
    renderer.draw_board(game)
    renderer.set_hover_pos(350)
    renderer.draw_board(game)
    game.make_move(3)
    renderer.draw_board(game)
