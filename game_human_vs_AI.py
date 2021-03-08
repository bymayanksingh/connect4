import sys

import pygame
from pygame.locals import KEYDOWN

from config import black, white
from connect_game import ConnectGame
from events import MouseClickEvent, MouseHoverEvent, bus
from game_data import GameData
from game_renderer import GameRenderer

from agents import RandomAgent
from random import choice


def quit():
    sys.exit()


def start():
    agent = RandomAgent()
    data = GameData()
    screen = pygame.display.set_mode(data.size)
    game = ConnectGame(data, GameRenderer(screen, data))

    game.print_board()
    game.draw()

    pygame.display.update()
    pygame.time.wait(1000)

    agent_turn = choice([0, 1])

    # Processes mouse and keyboard events, dispatching events to the event bus.
    # The events are handled by the ConnectGame and GameRenderer classes.
    while not game.game_data.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()

            if event.type == pygame.MOUSEMOTION:
                bus.emit("mouse:hover", game.renderer, MouseHoverEvent(event.pos[0]))

            if event.type == pygame.MOUSEBUTTONDOWN:
                bus.emit("mouse:click", game, MouseClickEvent(event.pos[0]))

            if event.type == KEYDOWN:
                if event.key == pygame.K_z:
                    mods: int = pygame.key.get_mods()
                    if mods & pygame.KMOD_CTRL:
                        bus.emit("game:undo", game)

            if data.turn == agent_turn and not game.game_data.game_over:
                game.do_movement(agent.get_move(data))
                game.update()
                game.draw()

            game.update()
            game.draw()


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_display(text, color, p, q, v):
    largeText = pygame.font.SysFont("monospace", v)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.center = (p, q)
    screen.blit(TextSurf, TextRect)


pygame.init()
screen = pygame.display.set_mode(GameData().size)
pygame.display.set_caption("Connect Four | Mayank Singh")
message_display("CONNECT FOUR!!", white, 350, 150, 75)
message_display("HAVE FUN!", (23, 196, 243), 350, 300, 75)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    def button(msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(screen, ac, (x, y, w, h))

            if click[0] == 1 and action is not None:
                action()
        else:
            pygame.draw.rect(screen, ic, (x, y, w, h))

        smallText = pygame.font.SysFont("monospace", 30)
        textSurf, textRect = text_objects(msg, smallText, white)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        screen.blit(textSurf, textRect)


    button("PLAY!", 150, 450, 100, 50, white, white, start)
    button("PLAY", 152, 452, 96, 46, black, black, start)
    button("QUIT", 450, 450, 100, 50, white, white, quit)
    button("QUIT", 452, 452, 96, 46, black, black, quit)
    pygame.display.update()
