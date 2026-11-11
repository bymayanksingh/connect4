import math
import os
import sys
import random

import pygame

from config import BLACK
from events import GameOver, MouseClickEvent, PieceDropEvent, bus
from game_data import GameData
from game_renderer import GameRenderer


class ConnectGame:
    """
    Holds all of the game logic and game data.
    """

    game_data: GameData
    renderer: GameRenderer

    def __init__(self, game_data: GameData, renderer: GameRenderer):
        """
        Initializes the connect game.
        :param game_data: A reference to the game data object.
        :param renderer: A reference to the game renderer.
        """
        self.game_data = game_data
        self.renderer = renderer
        
        # Flag to track if we've printed linear system for current turn
        self.printed_system_for_turn = False
        
        # Print the board state at the start
        self.print_board()
        
        # For modes with an agent, print initial linear system for the starting state
        if self.game_data.agent1 and self.game_data.game_mode in ['pva', 'ava']:
            print("\n=== Initial game state analysis ===")
            game_state = self.game_data.get_state_for_agent()
            
            # Print linear system for Player 1's initial decision
            print(f"\n=== Linear system for Player 1 (initial position) ===")
            self.game_data.agent1.analyze_position(self.game_data.agent1._convert_to_game_state(game_state))
            self.printed_system_for_turn = True

    def quit(self):
        """
        Exits the game.
        """
        sys.exit()

    def make_move(self, col: int, is_agent_move: bool = False) -> bool:
        """
        Make a move in the specified column.
        
        Args:
            col: The column to make the move in
            is_agent_move: Flag indicating if this move is being made by an agent
            
        Returns:
            bool: True if the move was successful, False otherwise
        """
        if self.game_data.game_board.is_valid_location(col):
            row = self.game_data.game_board.get_next_open_row(col)
            
            self.game_data.last_move_row.append(row)
            self.game_data.last_move_col.append(col)
            self.game_data.game_board.drop_piece(row, col, self.game_data.turn + 1)
            
            self.draw()
            bus.emit("piece:drop", PieceDropEvent(self.game_data.game_board.board[row][col]))
            self.print_board()
            
            # Reset the printed system flag because we've moved to a new turn
            self.printed_system_for_turn = False
            
            if self.game_data.game_board.winning_move(self.game_data.turn + 1):
                # Determine winning player and update agent reward if needed
                winning_player = self.game_data.turn + 1
                self.update_agent_reward(winning_player)
                
                bus.emit("game:over", self.renderer, GameOver(False, winning_player))
                self.game_data.game_over = True
                
            pygame.display.update()
            self.game_data.turn += 1
            self.game_data.turn = self.game_data.turn % 2
            return True
        return False
        
    def update_agent_reward(self, winning_player=None):
        """
        Update agent with reward based on game outcome.
        
        Args:
            winning_player: The player who won (1 or 2), or None if tie
        """
        if self.game_data.game_mode not in ['pva', 'ava']:
            return
            
        game_state = self.game_data.get_state_for_agent()
        
        # Determine reward based on outcome
        if winning_player is None:  # Tie
            reward = 0.0
            print("Game ended in a tie. Agent reward: 0.0")
        elif (winning_player == 2 and self.game_data.game_mode == 'pva') or \
             (self.game_data.game_mode == 'ava'):  # Agent win
            reward = 10.0
            print("Agent won! Reward: 10.0")
        else:  # Agent loss
            reward = -10.0
            print("Agent lost. Reward: -10.0")
            
        # Update agent with final reward
        if self.game_data.agent1:
            self.game_data.agent1.update(game_state, reward)
        
    @bus.on("mouse:click")
    def mouse_click(self, event: MouseClickEvent):
        """
        Handles a mouse click event.
        :param event: Data about the mouse click
        """
        pygame.draw.rect(
            self.renderer.screen,
            BLACK,
            (0, 0, self.game_data.width, self.game_data.sq_size),
        )
        
        col = int(math.floor(event.posx / self.game_data.sq_size))
        # Add bounds checking to ensure column is valid (0 to cols-1)
        if 0 <= col < self.game_data.game_board.cols:
            # Now make the move (removed linear system printing from here)
            self.make_move(col)
        # If col is outside valid range, ignore the click
        
    def handle_agent_move(self) -> None:
        """
        Handle agent moves when it's their turn.
        """
        if self.game_data.game_over:
            return
            
        current_agent = None
        player_number = None
        
        # For PVA mode, only handle agent's turn (Player 2)
        if self.game_data.game_mode == 'pva' and self.game_data.turn == 1:
            current_agent = self.game_data.agent1
            player_number = 2
        elif self.game_data.game_mode == 'ava':
            # For AVA mode, handle whichever player's turn it is
            player_number = self.game_data.turn + 1
            current_agent = self.game_data.agent1
            
        if current_agent:
            print(f"\n=== Agent thinking for Player {player_number} ===")
            
            # The choose_action method already prints the linear system
            game_state = self.game_data.get_state_for_agent()
            col = current_agent.choose_action(game_state)
            
            # Reset flag since we're making a move
            self.printed_system_for_turn = False
            
            # Validate column before making move
            if 0 <= col < self.game_data.game_board.cols:
                self.make_move(col, is_agent_move=True)
            else:
                print(f"Agent tried to make an invalid move: column {col}")
                # Choose a random valid column instead
                valid_cols = [c for c in range(self.game_data.game_board.cols) 
                             if self.game_data.game_board.is_valid_location(c)]
                if valid_cols:
                    col = random.choice(valid_cols)
                    self.make_move(col, is_agent_move=True)

    def update(self):
        """
        Checks the game state, dispatching events as needed.
        """
        # First, check if the game is over due to a tie
        if self.game_data.game_board.tie_move():
            # Update agent with tie reward
            self.update_agent_reward(None)
            
            bus.emit("game:over", self.renderer, GameOver(was_tie=True))
            self.game_data.game_over = True
            
        # If game is not over and it's a human player's turn,
        # print the linear system BEFORE they make a move
        if not self.game_data.game_over and not self.printed_system_for_turn:
            is_human_turn = False
            
            # Check if it's a human player's turn
            if self.game_data.game_mode == 'pvp':
                is_human_turn = True
            elif self.game_data.game_mode == 'pva' and self.game_data.turn == 0:
                is_human_turn = True
            
            # Print linear system for human turn
            if is_human_turn and self.game_data.agent1:
                game_state = self.game_data.get_state_for_agent()
                print(f"\n=== Linear system for Player {self.game_data.turn + 1} (make your move) ===")
                self.game_data.agent1.analyze_position(game_state)
                self.printed_system_for_turn = True
            
        # If game is not over, handle agent's turn
        if not self.game_data.game_over:
            self.handle_agent_move()
            
        # Handle game over state
        if self.game_data.game_over:
            print(os.getpid())
            pygame.time.wait(1000)
            
            # Instead of running game.py as a separate process, we'll restart the game
            # by quitting pygame and letting the Python script restart naturally
            # This ensures the window size is properly reset
            pygame.quit()
            
            # Use sys.executable to ensure we use the correct Python interpreter
            import sys
            script_dir = os.path.dirname(os.path.abspath(__file__))
            game_path = os.path.join(script_dir, "game.py")
            
            # Execute the game script with the proper Python interpreter
            os.execl(sys.executable, sys.executable, game_path)

    def draw(self):
        """
        Directs the game renderer to 'render' the game state to the audio and video devices.
        """
        self.renderer.draw(self.game_data)
        

    def print_board(self):
        """
        Prints the state of the board to the console.
        """
        self.game_data.game_board.print_board()
