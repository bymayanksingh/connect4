import pygame
from pygame.locals import KEYDOWN

from config import black, blue, white
from connect_game import ConnectGame
from events import MouseClickEvent, MouseHoverEvent, bus
from game_data import GameData
from game_renderer import GameRenderer
from config import black, blue, red, white, yellow, green

def quitgame():
    pygame.quit()
    quit()


def startgame():
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


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_display(text, color, p, q, v):
    Text = pygame.font.SysFont("monospace", v)
    TextSurf, TextRect = text_objects(text, Text, color)
    TextRect.center = (p, q)
    screen.blit(TextSurf, TextRect)


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
    message_display(msg, black, (x + (w / 2)), (y + (h / 2)), 30)


pygame.init()
screen = pygame.display.set_mode(GameData().size)
pygame.display.set_caption("Connect Four | Mayank Singh")
message_display("CONNECT FOUR", yellow, 350, 150, 75)
message_display("HAVE FUN!", (23, 196, 243), 350, 300, 75)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    button("PLAY", 125, 450, 150, 60, white, green, startgame)
    button("QUIT", 425, 450, 150, 60, white, red, quitgame)
    pygame.display.update()