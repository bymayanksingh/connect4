import sys

import pygame
from pygame.locals import KEYDOWN

from random import choice

from config import black, white
from connect_game import ConnectGame
from events import MouseClickEvent, MouseHoverEvent, bus
from game_data import GameData
from game_renderer import GameRenderer
from agents import MinimaxAgent


def quit():
    sys.exit()


def start_player_vs_player():
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
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_CTRL:
                        bus.emit("game:undo", game)

            game.update()
            game.draw()


def start_player_vs_ai():
    agent = MinimaxAgent()
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
                game.make_movement(agent.get_move(data))
                game.update()
                game.draw()

            game.update()
            game.draw()


def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_display(text, color, p, q, v, screen):
    large_text = pygame.font.SysFont("monospace", v)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (p, q)
    screen.blit(text_surf, text_rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode(GameData().size)
    pygame.display.set_caption("Connect Four | Mayank Singh")
    message_display("CONNECT FOUR!!", white, 350, 150, 75, screen)
    message_display("HAVE FUN!", (23, 196, 243), 350, 300, 75, screen)

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

        button("2 PLAYERS", 125, 450, 170, 50, white, white, start_player_vs_player)
        button("2 PLAYERS", 127, 452, 166, 46, black, black, start_player_vs_player)

        # button("AI", 300, 450, 100, 50, white, white, start_player_vs_ai)
        # button("AI", 302, 452, 96, 46, black, black, start_player_vs_ai)

        button("COMPUTER", 125, 510, 170, 50, white, white, start_player_vs_ai)
        button("AI", 127, 512, 166, 46, black, black, start_player_vs_ai)

        button("QUIT", 500, 450, 100, 50, white, white, quit)
        button("QUIT", 502, 452, 96, 46, black, black, quit)

        pygame.display.update()


if __name__ == "__main__":
    main()