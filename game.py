import sys

import pygame
from pygame.locals import KEYDOWN

from config import black, blue, gray, green, red, violet, white, yellow
from connect_game import ConnectGame
from events import MouseClickEvent, MouseHoverEvent, bus
from game_data import GameData
from game_renderer import GameRenderer

c1 = red
c2 = yellow


def quit():
    sys.exit()


def start():
    data = GameData(c1, c2)
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


flag = 1


def color_change():
    global screen, flag
    screen.fill(black)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        message_display("CONNECT FOUR!!", white, 350, 150, 75)
        message_display("PLAYER 1", c1, 215, 300, 35)
        message_display("PLAYER 2", c2, 215, 500, 35)

        button("", 100, 325, 30, 30, red, coin_change, 1)
        button("", 150, 325, 30, 30, yellow, coin_change, 1)
        button("", 200, 325, 30, 30, green, coin_change, 1)
        button("", 250, 325, 30, 30, blue, coin_change, 1)
        button("", 300, 325, 30, 30, violet, coin_change, 1)
        button("", 350, 325, 30, 30, gray, coin_change, 1)

        button("", 100, 525, 30, 30, red, coin_change, 2)
        button("", 150, 525, 30, 30, yellow, coin_change, 2)
        button("", 200, 525, 30, 30, green, coin_change, 2)
        button("", 250, 525, 30, 30, blue, coin_change, 2)
        button("", 300, 525, 30, 30, violet, coin_change, 2)
        button("", 350, 525, 30, 30, gray, coin_change, 2)

        button("SAVE", 510, 600, 130, 50, white, save)
        button("SAVE", 512, 602, 125, 46, black, save)
        pygame.display.update()

        if flag == 0:
            flag = 1
            screen.fill(black)
            message_display("CONNECT FOUR!!", white, 350, 150, 75)
            message_display("HAVE FUN!", (23, 196, 243), 350, 300, 75)
            running = False


def save():
    global flag
    flag = 0


def coin_change(color, player_no):
    global c1, c2

    if player_no == 1:
        c1 = color
    else:
        c2 = color


def button(msg, x, y, w, h, color, action=None, player_no=0):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, color, (x, y, w, h))

        if click[0] == 1 and action != None:
            if action == coin_change:
                action(color, player_no)
            else:
                action()
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))

    smallText = pygame.font.SysFont("monospace", 30)
    textSurf, textRect = text_objects(msg, smallText, white)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)


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

    button("PLAY!", 150, 450, 100, 50, white, start)
    button("PLAY", 152, 452, 96, 46, black, start)
    button("QUIT", 450, 450, 100, 50, white, quit)
    button("QUIT", 452, 452, 96, 46, black, quit)
    button("COLOR CHANGE", 210, 600, 230, 50, white, color_change)
    button("COLOR CHANGE", 212, 602, 225, 46, black, color_change)
    pygame.display.update()
