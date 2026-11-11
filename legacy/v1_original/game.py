import sys

import pygame
from pygame.locals import KEYDOWN

from config import BLACK, BLUE, WHITE, RED, GREEN, YELLOW
from connect_game import ConnectGame
from events import MouseClickEvent, MouseHoverEvent, bus
from game_data import GameData
from game_renderer import GameRenderer, console


def quit():
    sys.exit()


def start(mode: str = 'pvp', board_size: tuple = None):
    data = GameData()
    
    # Set board size if specified (columns, rows, win_condition)
    if board_size:
        cols, rows, win_condition = board_size
        data.set_board_size(cols, rows, win_condition)
    
    data.set_game_mode(mode)
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

            if event.type == pygame.MOUSEBUTTONDOWN:
                bus.emit("mouse:click", game, MouseClickEvent(event.pos[0]))

            if event.type == KEYDOWN:
                if event.key == pygame.K_z:
                    mods: int = pygame.key.get_mods()
                    if mods & pygame.KMOD_CTRL:
                        bus.emit("game:undo", game)

            if event.type == pygame.MOUSEWHEEL:
                game.renderer.scroll_index -= event.y
                max_start = max(0, len(console.lines) - game.renderer.line_height)
                game.renderer.scroll_index = max(0, min(game.renderer.scroll_index, max_start))
        
        # Update game state regardless of events
        game.update()
        game.draw()
        pygame.display.update()


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_display(text, color, p, q, v):
    largeText = pygame.font.SysFont("monospace", v)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.center = (p, q)
    screen.blit(TextSurf, TextRect)


pygame.init()
# Always use the default 7x6 board size for the main menu
default_data = GameData()
# Force the default game data to use standard size board for menu
default_data.set_board_size(7, 6, 4)  # Standard Connect 4 dimensions
screen = pygame.display.set_mode(default_data.size)
pygame.display.set_caption("Connect Four | Mayank Singh")

# Menu state variables
selected_size = (7, 6, 4)  # Default: 7x6 Connect 4 (cols, rows, win_condition)
selected_mode = 'pvp'  # Default: Player vs Player
menu_state = 'main'  # States: 'main', 'size', 'mode'

# Add variable to track if mouse button was just released
button_clicked = False
prev_mouse_state = pygame.mouse.get_pressed()[0]
transition_delay = 0  # Counter for delaying action after menu transition

running = True
while running:
    # Clear screen
    screen.fill(BLACK)
    
    # Title
    message_display("CONNECT FOUR!", WHITE, 350, 100, 75)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Check for mouse button release (single click)
    current_mouse_state = pygame.mouse.get_pressed()[0]
    
    # Set button_clicked to True when mouse is released (goes from pressed to not pressed)
    if prev_mouse_state and not current_mouse_state:
        button_clicked = True
    else:
        button_clicked = False
    
    # Update previous mouse state for next frame
    prev_mouse_state = current_mouse_state
    
    # Decrement transition delay counter if active
    if transition_delay > 0:
        transition_delay -= 1
    
    def button(msg, x, y, w, h, ic, ac, action=None, selected=False):
        global transition_delay
        mouse = pygame.mouse.get_pos()
        
        # Check if mouse is over button
        is_over_button = x + w > mouse[0] > x and y + h > mouse[1] > y
        
        # Determine button color based on hover
        button_color = ac if is_over_button else ic
        
        # If this button is selected, draw a highlight
        if selected:
            pygame.draw.rect(screen, GREEN, (x-5, y-5, w+10, h+10))
            
        pygame.draw.rect(screen, button_color, (x, y, w, h))
        # Draw slightly smaller black rectangle inside
        pygame.draw.rect(screen, BLACK, (x+2, y+2, w-4, h-4))

        smallText = pygame.font.SysFont("monospace", 30)
        textSurf, textRect = text_objects(msg, smallText, WHITE)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        screen.blit(textSurf, textRect)
        
        # Only trigger action on mouse button release and when transition delay is inactive
        if is_over_button and button_clicked and action is not None and transition_delay == 0:
            # Set transition delay to prevent immediate clicks after state change
            transition_delay = 5  # Delay for 5 frames
            action()
            return True
        return False

    # Settings indicator
    current_settings_text = f"Game: {'4x3 Connect 3' if selected_size == (4, 3, 3) else '7x6 Connect 4'} | Mode: {selected_mode.upper()}"
    message_display(current_settings_text, YELLOW, 350, 180, 25)
    
    button_width = 450
    button_height = 50
    button_x = (700 - button_width) // 2  # Center horizontally
    
    if menu_state == 'main':
        # Main menu options
        message_display("SELECT GAME OPTIONS", WHITE, 350, 250, 40)
        button("Board Size", button_x, 300, button_width, button_height, WHITE, BLUE, 
               lambda: globals().update(menu_state='size'))
        button("Game Mode", button_x, 370, button_width, button_height, WHITE, BLUE, 
               lambda: globals().update(menu_state='mode'))
        button("START GAME", button_x, 470, button_width, button_height, WHITE, GREEN, 
               lambda: start(selected_mode, selected_size))
        
    elif menu_state == 'size':
        # Board size selection menu
        message_display("SELECT BOARD SIZE", WHITE, 350, 250, 40)
        button("7x6 Connect 4 (Standard)", button_x, 300, button_width, button_height, 
               WHITE, BLUE, lambda: globals().update(selected_size=(7, 6, 4), menu_state='main'),
               selected=(selected_size == (7, 6, 4)))
        button("4x3 Connect 3 (Mini)", button_x, 370, button_width, button_height, 
               WHITE, BLUE, lambda: globals().update(selected_size=(4, 3, 3), menu_state='main'),
               selected=(selected_size == (4, 3, 3)))
        button("Back", button_x, 470, button_width, button_height, WHITE, RED, 
               lambda: globals().update(menu_state='main'))
        
    elif menu_state == 'mode':
        # Game mode selection menu
        message_display("SELECT GAME MODE", WHITE, 350, 250, 40)
        button("Player vs Player", button_x, 300, button_width, button_height, 
               WHITE, BLUE, lambda: globals().update(selected_mode='pvp', menu_state='main'),
               selected=(selected_mode == 'pvp'))
        button("Player vs Agent", button_x, 370, button_width, button_height, 
               WHITE, BLUE, lambda: globals().update(selected_mode='pva', menu_state='main'),
               selected=(selected_mode == 'pva'))
        button("Agent vs Agent", button_x, 440, button_width, button_height, 
               WHITE, BLUE, lambda: globals().update(selected_mode='ava', menu_state='main'),
               selected=(selected_mode == 'ava'))
        button("Back", button_x, 510, button_width, button_height, WHITE, RED, 
               lambda: globals().update(menu_state='main'))
        
    # Quit button - always visible
    quit_width = 150
    quit_x = (700 - quit_width) // 2
    button("QUIT", quit_x, 610, quit_width, button_height, WHITE, RED, quit)
    
    pygame.display.update()
