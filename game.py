import pygame
from pygame.locals import KEYDOWN

from connect_game import ConnectGame
from events import MouseClickEvent, MouseHoverEvent, bus
from game_data import GameData
from game_renderer import GameRenderer

pygame.init()

data = GameData()
screen = pygame.display.set_mode(data.size)
game = ConnectGame(data, GameRenderer(screen, data))


game.print_board()
game.draw()

pygame.display.update()
pygame.time.wait(1000)


# Processes mouse and keyboard events, dispatching events to the event bus.
# The events are handled by the ConnectGame and GameRenderer classes.
while not game.game_data.game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.quit()

        if event.type == pygame.MOUSEMOTION:
            bus.emit("mouse:hover", game.renderer, MouseHoverEvent(event.pos[0]))

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            bus.emit("mouse:click", game, MouseClickEvent(event.pos[0]))

        if event.type == KEYDOWN:
            if event.key == pygame.K_z:
                mods: int = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL:
                    bus.emit("game:undo", game)

        game.update()
        game.draw()
