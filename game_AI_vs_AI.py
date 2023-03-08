import sys

import pygame

from config import black, white
from connect_game import ConnectGame
from game_data import GameData
from game_renderer import GameRenderer

from agents import MinimaxAgent, RandomAgent
from time import sleep


def quit():
    sys.exit()


def start():
    agent1 = MinimaxAgent()  # red
    agent2 = RandomAgent()  # yellow

    delay = 0.5
    data = GameData()
    screen = pygame.display.set_mode(data.size)
    game = ConnectGame(data, GameRenderer(screen, data))

    game.print_board()
    game.draw()

    pygame.display.update()
    pygame.time.wait(10)

    agent1_turn = 0

    # Processes mouse and keyboard events, dispatching events to the event bus.
    # The events are handled by the ConnectGame and GameRenderer classes.
    while not game.game_data.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()

            sleep(delay)
            if data.turn == agent1_turn and not game.game_data.game_over:
                game.make_movement(agent1.get_move(data))
                game.update()
                game.draw()
            else:
                game.make_movement(agent2.get_move(data))
                game.update()
                game.draw()

            game.update()
            game.draw()


def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_display(text, color, p, q, v):
    large_text = pygame.font.SysFont("monospace", v)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (p, q)
    screen.blit(text_surf, text_rect)


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

        small_text = pygame.font.SysFont("monospace", 30)
        text_surf, text_rect = text_objects(msg, small_text, white)
        text_rect.center = ((x + (w / 2)), (y + (h / 2)))
        screen.blit(text_surf, text_rect)


    button("PLAY!", 150, 450, 100, 50, white, white, start)
    button("PLAY", 152, 452, 96, 46, black, black, start)
    button("QUIT", 450, 450, 100, 50, white, white, quit)
    button("QUIT", 452, 452, 96, 46, black, black, quit)
    pygame.display.update()
