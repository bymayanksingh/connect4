import sys

import pygame
from pygame.locals import KEYDOWN

from config import black, blue, gray, green, red, violet, white, yellow
from connect_game import ConnectGame
from events import MouseClickEvent, MouseHoverEvent, bus
from game_data import GameData
from game_renderer import GameRenderer


def quit():
    ''' 
    To exit game
    '''
    sys.exit()


def start():
    '''
    Main Game Loop
    '''
    data = GameData(c1, c2 ,bg)
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
    restart()


def restart():
    '''
    Use to show the menu after game is finished
    '''
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        button("RESTART", 275, 200, 150, 50, white, start)
        button("RESTART", 277, 202, 146, 46, black, start)
        button("CHANGE COLORS", 230, 350, 250, 50, white, menu)
        button("CHANGE COLORS", 232, 352, 246, 46, black, menu)
        button("QUIT", 300, 500, 100, 50, white, quit)
        button("QUIT", 302, 502, 96, 46, black, quit)
        pygame.display.update()

    

def color_change(color, player_no):
    '''
    Used to change colors of player coins and background
    '''
    global c1, c2 ,bg

    if player_no == 1:
        c1 = color
    elif player_no == 2:
        c2 = color
    else :
        bg = color

def button(msg, x, y, w, h, color, action=None, player_no=0):
    '''
    Used to make buttons which fires when clicked and performs the designated action
    '''
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, color, (x, y, w, h))

        if click[0] == 1 and action != None:
            if action == color_change:
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
    '''
    Used to make text for objects
    '''
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_display(text, color, p, q, v):
    '''
    Used to make the message display on screen
    '''
    largeText = pygame.font.SysFont("monospace", v)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.center = (p, q)
    screen.blit(TextSurf, TextRect)


pygame.init()

c1 = red
c2 = yellow
bg = blue

screen = pygame.display.set_mode(GameData().size)
pygame.display.set_caption("Connect Four | Mayank Singh")
logo = pygame.image.load("images/logo/connect4.png")

def menu():
    '''
    Menu Loop
    '''
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.Surface.fill(screen,black)
        message_display("PLAYER 1", c1, 210, 250, 45)
        message_display("PLAYER 2", c2, 210, 400, 45)
        message_display("BOARD COLOR", bg, 233, 550, 40)

        button("PLAY!", 500, 300, 100, 50, white, start)
        button("PLAY!", 502, 302, 96, 46, black, start)
        button("QUIT", 500, 450, 100, 50, white, quit)
        button("QUIT", 502, 452, 96, 46, black, quit)

        button("", 100, 280, 30, 30, red, color_change, 1)
        button("", 150, 280, 30, 30, yellow, color_change, 1)
        button("", 200, 280, 30, 30, green, color_change, 1)
        button("", 250, 280, 30, 30, blue, color_change, 1)
        button("", 300, 280, 30, 30, violet, color_change, 1)
        button("", 350, 280, 30, 30, gray, color_change, 1)

        button("", 100, 430, 30, 30, red, color_change, 2)
        button("", 150, 430, 30, 30, yellow, color_change, 2)
        button("", 200, 430, 30, 30, green, color_change, 2)
        button("", 250, 430, 30, 30, blue, color_change, 2)
        button("", 300, 430, 30, 30, violet, color_change, 2)
        button("", 350, 430, 30, 30, gray, color_change, 2)

        button("", 100, 580, 30, 30, red, color_change, None)
        button("", 150, 580, 30, 30, yellow, color_change, None)
        button("", 200, 580, 30, 30, green, color_change, None)
        button("", 250, 580, 30, 30, blue, color_change, None)
        button("", 300, 580, 30, 30, violet, color_change, None)
        button("", 350, 580, 30, 30, gray, color_change, None) 

        screen.blit(logo,(50,50))
        pygame.display.update()
menu()