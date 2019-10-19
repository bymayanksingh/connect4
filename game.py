from typing import Tuple

import pygame

from pygame.locals import KEYDOWN
from connect_game import ConnectGame
from game_data import GameData
from graphics import GameRenderer


pygame.init()

data = GameData()
screen = pygame.display.set_mode(data.size)
game = ConnectGame(data, GameRenderer(screen, data))



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

        game.update()
        game.draw()
