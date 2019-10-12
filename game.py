import os

from typing import Tuple

import pygame

from pygame.locals import KEYDOWN
from connect_game import ConnectGame
from game_data import GameData
from graphics import GameRenderer

sq_size: int = 100

width: int = 7 * sq_size
height: int = 7 * sq_size
size: Tuple[int, int] = (width, height)
radius: int = int(sq_size / 2 - 5)

pygame.init()
screen = pygame.display.set_mode(size)

game = ConnectGame(GameData(), GameRenderer(screen))

game.print_board()
game.draw()

pygame.display.update()
pygame.time.wait(1000)

while not game.game_data.game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.quit()

        if event.type == pygame.MOUSEMOTION:
            game.mouse_move(event.pos[0])

        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.mouse_click(event.pos[0])

        if event.type == KEYDOWN:
            if event.key == pygame.K_z:
                mods: int = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL:
                    game.undo()
        # tie

        game.update()
        game.draw()