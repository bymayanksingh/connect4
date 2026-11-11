from typing import Any, Dict, List, Tuple, Set, Optional
import numpy as np
import copy
from game_board import GameBoard

class GameState:
    """
    A wrapper class for game states that supports hashing and comparison.
    This enables using GameState objects as dictionary keys for the MDP value function.
    """
    
    def __init__(self, board: np.ndarray, turn: int, game_board: GameBoard = None):
        """
        Initialize a game state.
        
        Args:
            board: The game board as a numpy array
            turn: The player's turn (0 or 1)
            game_board: Reference to GameBoard object (if available)
        """
        self.board = board.copy()  # Make a copy to ensure independence
        self.turn = turn
        
        # Create a new GameBoard if none provided
        if game_board is None:
            # Get board dimensions from the array
            rows, cols = board.shape
            self.game_board = GameBoard(rows=rows, cols=cols)
            self.game_board.board = board.copy()
        else:
            self.game_board = game_board
            
    def __hash__(self):
        """
        Generate a hash for the game state based on board configuration and turn.
        This allows GameState objects to be used as dictionary keys.
        """
        # Convert board to tuple for hashing
        board_tuple = tuple(map(tuple, self.board))
        return hash((board_tuple, self.turn))
        
    def __eq__(self, other):
        """Check if two game states are equal."""
        if not isinstance(other, GameState):
            return False
        return (np.array_equal(self.board, other.board) and 
                self.turn == other.turn)
                
    def is_terminal(self) -> bool:
        """Check if this is a terminal state (win or draw)."""
        # Check if previous player won
        last_player = 3 - (self.turn + 1)  # Convert from 0/1 to 1/2
        if self.game_board.winning_move(last_player):
            return True
            
        # Check for a draw
        if self.game_board.tie_move():
            return True
            
        return False
        
    def get_valid_actions(self) -> List[int]:
        """Get valid actions (columns) for this state."""
        # Use game_board's columns count instead of hardcoded 7
        return [col for col in range(self.game_board.cols) if self.game_board.is_valid_location(col)]
    
    def apply_action(self, action: int) -> 'GameState':
        """
        Apply an action to this state and return the resulting state.
        
        Args:
            action: Column to drop piece in (0-6)
            
        Returns:
            GameState: The new state after action
        """
        # Create a new game board for the next state
        new_board = self.board.copy()
        
        # Create a new game board object with the same dimensions and win condition
        rows, cols = self.board.shape
        win_condition = getattr(self.game_board, 'win_condition', 4)  # Default to 4 if not available
        new_game_board = GameBoard(rows=rows, cols=cols, win_condition=win_condition)
        new_game_board.board = new_board
        
        # Find the next open row in the chosen column
        row = new_game_board.get_next_open_row(action)
        
        # Place the piece
        new_board[row][action] = self.turn + 1  # Convert from 0/1 to 1/2
        
        # Create and return the new state with updated turn
        return GameState(new_board, (self.turn + 1) % 2, new_game_board)
        
    def get_key(self) -> str:
        """
        Get a string key representation for this state.
        Used for debugging and display purposes only.
        """
        # Convert the board to a string representation
        cols = []
        num_rows, num_cols = self.board.shape
        for col in range(num_cols):
            column = ''.join(str(int(self.board[row][col])) for row in range(num_rows))
            cols.append(column)
        
        # Join columns with '|' separator and combine with turn
        return f"{self.turn}:{':'.join(cols)}"
        
    def check_for_immediate_threat(self, player: int) -> List[int]:
        """
        Check if there are any immediate threats (opponent can win next move).
        
        Args:
            player: The player to check threats for
            
        Returns:
            List[int]: List of columns where the player can win immediately
        """
        winning_moves = []
        board = self.board
        num_rows, num_cols = board.shape
        win_condition = self.game_board.win_condition
        
        # Check each column
        for col in range(num_cols):
            # Skip if column is full
            if not self.game_board.is_valid_location(col):
                continue
                
            # Create a temporary board with correct dimensions and win condition
            temp_board = board.copy()
            temp_game_board = GameBoard(rows=num_rows, cols=num_cols, win_condition=win_condition)
            temp_game_board.board = temp_board
            
            # Find the next open row in this column
            row = temp_game_board.get_next_open_row(col)
            
            # Place the piece
            temp_board[row][col] = player
            
            # Check if this creates a win
            if temp_game_board.winning_move(player):
                winning_moves.append(col)
                
        return winning_moves
        
    def check_for_traps(self, player: int) -> List[int]:
        """
        Check for common Connect Four trap setups that lead to forced wins.
        
        Args:
            player: The player to check traps for
            
        Returns:
            List[int]: List of columns to play to set up or block traps
        """
        trap_moves = []
        opponent = 3 - player
        board = self.board
        num_rows, num_cols = board.shape
        win_condition = self.game_board.win_condition  # Get win condition from game board
        
        # Special handling for early game center control
        empty_count = np.count_nonzero(board == 0)
        total_slots = num_rows * num_cols
        is_early_game = empty_count > total_slots * 0.8  # First few moves (80% empty)
        
        # In early game, prioritize center and adjacent columns
        if is_early_game:
            # Center column is highly valuable
            center_col = num_cols // 2
            if self.game_board.is_valid_location(center_col):
                if center_col not in trap_moves:
                    trap_moves.append(center_col)
            
            # If opponent has center, control adjacent columns
            if center_col < num_cols and board[0][center_col] == opponent:
                for col in [center_col-1, center_col+1]:
                    if 0 <= col < num_cols and self.game_board.is_valid_location(col) and col not in trap_moves:
                        trap_moves.append(col)
        
        # Find moves that create TWO threats simultaneously (true forks)
        for col in range(num_cols):
            if not self.game_board.is_valid_location(col):
                continue
                
            # Simulate placing a piece in this column
            row = self.game_board.get_next_open_row(col)
            temp_board = board.copy()
            temp_game_board = GameBoard(rows=num_rows, cols=num_cols, win_condition=win_condition)
            temp_game_board.board = temp_board
            temp_board[row][col] = player
            
            # Count threats at this position
            threats = 0
            
            # Check horizontal threats
            for c in range(max(0, col-(win_condition-1)), min(col+1, num_cols-(win_condition-1))):
                if c + win_condition <= num_cols:
                    window = [temp_board[row][c+i] for i in range(win_condition)]
                    if window.count(player) == win_condition - 1 and window.count(0) == 1:
                        threats += 1
            
            # Check vertical threats
            if row >= win_condition - 1:
                window = [temp_board[row-i][col] for i in range(win_condition)]
                if window.count(player) == win_condition - 1 and window.count(0) == 1:
                    threats += 1
                    
            # Check diagonal threats
            for i in range(win_condition):
                # Positive diagonal
                r = row - i
                c = col - i
                if r >= 0 and r <= num_rows - win_condition and c >= 0 and c <= num_cols - win_condition:
                    window = [temp_board[r+j][c+j] for j in range(win_condition)]
                    if window.count(player) == win_condition - 1 and window.count(0) == 1:
                        threats += 1
                
                # Negative diagonal
                r = row - i
                c = col + i
                if r >= 0 and r <= num_rows - win_condition and c >= win_condition - 1 and c < num_cols:
                    if all(0 <= r+j < num_rows and 0 <= c-j < num_cols for j in range(win_condition)):
                        window = [temp_board[r+j][c-j] for j in range(win_condition)]
                        if window.count(player) == win_condition - 1 and window.count(0) == 1:
                            threats += 1
            
            # Only consider as trap if it creates MULTIPLE threats
            if threats >= 2 and col not in trap_moves:
                trap_moves.append(col)
                
        return trap_moves
        
    def check_diagonal_connectivity(self, player: int) -> int:
        """
        Specifically check for diagonal connections and potential winning patterns.
        
        Args:
            player: The player to check for
            
        Returns:
            int: Score representing strength of diagonal connections
        """
        board = self.board
        num_rows, num_cols = board.shape
        score = 0
        opponent = 3 - player
        win_condition = self.game_board.win_condition
        
        # Check all possible diagonal directions
        # Positive diagonals (/)
        for row in range(num_rows - (win_condition - 1)):
            for col in range(num_cols - (win_condition - 1)):
                window = [board[row+i][col+i] for i in range(win_condition)]
                # Give points for our pieces, subtract for opponent pieces
                player_count = window.count(player)
                opponent_count = window.count(opponent)
                empty_count = window.count(0)
                
                # Only consider if there are no opponent pieces (can't win otherwise)
                if opponent_count == 0:
                    if player_count == win_condition - 1 and empty_count == 1:
                        score += 5  # Near win
                    elif player_count == win_condition - 2 and empty_count == 2:
                        score += 2  # Building threat
                    elif player_count == 1 and empty_count == win_condition - 1:
                        score += 0.5  # Starting position
                
                # Also check opponent's diagonal threats
                if player_count == 0:
                    if opponent_count == win_condition - 1 and empty_count == 1:
                        score -= 6  # Near loss - weigh higher than our threats
                    elif opponent_count == win_condition - 2 and empty_count == 2:
                        score -= 3  # Opponent building threat
        
        # Negative diagonals (\)
        for row in range(win_condition - 1, num_rows):
            for col in range(num_cols - (win_condition - 1)):
                window = [board[row-i][col+i] for i in range(win_condition)]
                # Give points for our pieces, subtract for opponent pieces
                player_count = window.count(player)
                opponent_count = window.count(opponent)
                empty_count = window.count(0)
                
                # Only consider if there are no opponent pieces (can't win otherwise)
                if opponent_count == 0:
                    if player_count == win_condition - 1 and empty_count == 1:
                        score += 5  # Near win
                    elif player_count == win_condition - 2 and empty_count == 2:
                        score += 2  # Building threat
                    elif player_count == 1 and empty_count == win_condition - 1:
                        score += 0.5  # Starting position
                
                # Also check opponent's diagonal threats
                if player_count == 0:
                    if opponent_count == win_condition - 1 and empty_count == 1:
                        score -= 6  # Near loss - weigh higher than our threats
                    elif opponent_count == win_condition - 2 and empty_count == 2:
                        score -= 3  # Opponent building threat
        
        return score
        
    def detect_advanced_patterns(self, player: int) -> Tuple[List[int], float]:
        """
        Detect advanced Connect Four patterns beyond basic threats.
        
        Args:
            player: The player to check patterns for
            
        Returns:
            Tuple[List[int], float]: List of recommended moves and pattern score
        """
        opponent = 3 - player
        moves = []
        pattern_score = 0
        board = self.board
        num_rows, num_cols = board.shape
        win_condition = self.game_board.win_condition
        
        # Check for double-threat creation (placing a piece that creates TWO three-in-a-rows)
        for col in range(num_cols):
            if not self.game_board.is_valid_location(col):
                continue
                
            # Find where the piece would land
            row = self.game_board.get_next_open_row(col)
            
            # Create a temporary board with this move
            temp_board = board.copy()
            temp_board[row][col] = player
            
            # Count threats in all directions
            threat_count = 0
            
            # Check horizontal threats
            for c in range(max(0, col-(win_condition-1)), min(col+1, num_cols-(win_condition-1))):
                if c + win_condition <= num_cols:
                    window = [temp_board[row][c+i] for i in range(win_condition)]
                    if window.count(player) == win_condition - 1 and window.count(0) == 1:
                        threat_count += 1
            
            # Check vertical threats
            if row >= win_condition - 1:
                window = [temp_board[row-i][col] for i in range(win_condition)]
                if window.count(player) == win_condition - 1 and window.count(0) == 1:
                    threat_count += 1
            
            # Check diagonal threats
            # Positive diagonal
            for i in range(win_condition):
                r = row - i
                c = col - i
                if r >= 0 and r <= num_rows - win_condition and c >= 0 and c <= num_cols - win_condition:
                    window = [temp_board[r+j][c+j] for j in range(win_condition)]
                    if window.count(player) == win_condition - 1 and window.count(0) == 1:
                        threat_count += 1
            
            # Negative diagonal
            for i in range(win_condition):
                r = row - i
                c = col + i
                if r >= 0 and r <= num_rows - win_condition and c >= win_condition - 1 and c < num_cols:
                    if all(0 <= r+j < num_rows and 0 <= c-j < num_cols for j in range(win_condition)):
                        window = [temp_board[r+j][c-j] for j in range(win_condition)]
                        if window.count(player) == win_condition - 1 and window.count(0) == 1:
                            threat_count += 1
            
            # If this creates multiple threats, it's a very strong move
            if threat_count >= 2:
                moves.append(col)
                pattern_score += threat_count * 7  # Valuable move
        
        return moves, pattern_score 