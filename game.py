import math
import os
import sys
from typing import Tuple

import pygame

from pygame import mixer
from pygame.gfxdraw import aacircle, filled_circle
from pygame.locals import KEYDOWN


from config import *
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
        if game.game_data.game_board.tie_move():
            mixer.music.load(os.path.join("sounds", "event.ogg"))
            mixer.music.play(0)
            game.game_data.game_over = True

            game.renderer.myfont = pygame.font.SysFont("monospace", 75)
            game.renderer.label = game.renderer.myfont.render("GAME DRAW !!!!", 1, white)
            screen.blit(game.renderer.label, (40, 10))
            pygame.display.update()

        if game.game_data.game_over:
            # print(os.getpid())
            pygame.time.wait(3000)
            #os.system("kill " + str(os.getpid()))
            #os.system("./restart.sh")

        game.draw()