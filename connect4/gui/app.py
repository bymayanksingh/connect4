from __future__ import annotations

import math
import sys
import time
from typing import Optional, Tuple
import pygame

from connect4.ai.factory import AgentFactory
from connect4.board import GameBoard
from connect4.config import (
    BLACK,
    BLUE,
    BOARD_PRESETS,
    COLOR_THEMES,
    DEFAULT_FPS,
    DEFAULT_SQ_SIZE,
    GREEN,
    LIGHT_BLUE,
    RED,
    WHITE,
    YELLOW,
)
from connect4.game import Connect4Game
from connect4.gui.assets import assets
from connect4.gui.menu import Button
from connect4.gui.renderer import GameRenderer
from connect4.types import AIDifficulty, BoardDimensions, GameMode, GameStatus, Player


class Connect4App:
    """
    Main GUI application controller for Connect 4.
    Orchestrates screen transitions, user interactions, AI background turns,
    and rendering cycles.
    """

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Connect Four | Production Edition")
        self.clock = pygame.time.Clock()

        # Session configuration
        self.dimensions = BoardDimensions(cols=7, rows=6, win_condition=4)
        self.mode = GameMode.PVA
        self.ai_difficulty = AIDifficulty.MEDIUM
        self.p1_theme = "red"
        self.p2_theme = "yellow"
        self.board_color = BLUE
        self.sq_size = DEFAULT_SQ_SIZE

        # Initial window size for menu
        self.screen_width = 700
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = pygame.font.SysFont("monospace", 28, bold=True)
        self.title_font = pygame.font.SysFont("monospace", 48, bold=True)

        self.state = "MENU"  # 'MENU', 'SIZE', 'MODE', 'THEME', 'PLAYING', 'GAME_OVER'
        self.game: Optional[Connect4Game] = None
        self.renderer: Optional[GameRenderer] = None

    def start_game(self) -> None:
        """Initializes a new gameplay session and sets up geometry."""
        agent1 = None
        agent2 = None

        if self.mode == GameMode.PVA:
            agent2 = AgentFactory.create_agent(self.ai_difficulty, name=f"AI ({self.ai_difficulty.value.title()})")
        elif self.mode == GameMode.AVA:
            agent1 = AgentFactory.create_agent(AIDifficulty.HARD, name="AI P1 (Hard)")
            agent2 = AgentFactory.create_agent(self.ai_difficulty, name=f"AI P2 ({self.ai_difficulty.value.title()})")

        self.game = Connect4Game(
            dimensions=self.dimensions,
            mode=self.mode,
            agent1=agent1,
            agent2=agent2,
        )

        board_width = self.dimensions.cols * self.sq_size
        board_height = (self.dimensions.rows + 1) * self.sq_size

        self.screen = pygame.display.set_mode((board_width, board_height))
        self.renderer = GameRenderer(
            screen=self.screen,
            sq_size=self.sq_size,
            p1_theme=self.p1_theme,
            p2_theme=self.p2_theme,
            board_color=self.board_color,
        )
        self.state = "PLAYING"

    def run(self) -> None:
        """Main game application execution loop."""
        running = True
        while running:
            if self.state == "MENU":
                running = self._run_main_menu()
            elif self.state == "SIZE":
                running = self._run_size_menu()
            elif self.state == "MODE":
                running = self._run_mode_menu()
            elif self.state == "THEME":
                running = self._run_theme_menu()
            elif self.state in ("PLAYING", "GAME_OVER"):
                running = self._run_gameplay()

        pygame.quit()

    def _run_main_menu(self) -> bool:
        self.screen.fill(BLACK)
        title_surf = self.title_font.render("CONNECT FOUR", True, WHITE)
        self.screen.blit(title_surf, title_surf.get_rect(center=(350, 90)))

        settings_str = f"Board: {self.dimensions.cols}x{self.dimensions.rows} (K={self.dimensions.win_condition}) | Mode: {self.mode.value.upper()}"
        sub_surf = self.font.render(settings_str, True, YELLOW)
        self.screen.blit(sub_surf, sub_surf.get_rect(center=(350, 160)))

        buttons = [
            Button("START GAME", 175, 230, 350, 55, lambda: self.start_game(), color=GREEN, hover_color=WHITE),
            Button("Board Dimensions", 175, 305, 350, 50, lambda: self._set_state("SIZE")),
            Button("Game Mode & AI", 175, 375, 350, 50, lambda: self._set_state("MODE")),
            Button("Themes & Colors", 175, 445, 350, 50, lambda: self._set_state("THEME")),
            Button("QUIT", 225, 545, 250, 50, lambda: sys.exit(0), color=RED, hover_color=WHITE),
        ]

        for btn in buttons:
            btn.draw(self.screen, self.font)

        pygame.display.flip()
        self.clock.tick(DEFAULT_FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            for btn in buttons:
                if btn.handle_event(event):
                    break
        return True

    def _run_size_menu(self) -> bool:
        self.screen.fill(BLACK)
        title_surf = self.title_font.render("BOARD DIMENSIONS", True, WHITE)
        self.screen.blit(title_surf, title_surf.get_rect(center=(350, 90)))

        buttons = [
            Button("Standard 7x6 (Connect 4)", 175, 200, 350, 50,
                   lambda: self._set_dims(7, 6, 4),
                   selected=(self.dimensions == BoardDimensions(7, 6, 4))),
            Button("Mini 4x3 (Connect 3)", 175, 270, 350, 50,
                   lambda: self._set_dims(4, 3, 3),
                   selected=(self.dimensions == BoardDimensions(4, 3, 3))),
            Button("Large 8x7 (Connect 4)", 175, 340, 350, 50,
                   lambda: self._set_dims(8, 7, 4),
                   selected=(self.dimensions == BoardDimensions(8, 7, 4))),
            Button("Challenge 7x6 (Connect 5)", 175, 410, 350, 50,
                   lambda: self._set_dims(7, 6, 5),
                   selected=(self.dimensions == BoardDimensions(7, 6, 5))),
            Button("Back to Menu", 225, 510, 250, 50, lambda: self._set_state("MENU"), color=RED),
        ]

        for btn in buttons:
            btn.draw(self.screen, self.font)

        pygame.display.flip()
        self.clock.tick(DEFAULT_FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            for btn in buttons:
                if btn.handle_event(event):
                    break
        return True

    def _run_mode_menu(self) -> bool:
        self.screen.fill(BLACK)
        title_surf = self.title_font.render("MODE & DIFFICULTY", True, WHITE)
        self.screen.blit(title_surf, title_surf.get_rect(center=(350, 80)))

        buttons = [
            Button("Player vs Player (PvP)", 175, 170, 350, 48,
                   lambda: setattr(self, "mode", GameMode.PVP),
                   selected=(self.mode == GameMode.PVP)),
            Button("Player vs AI (PvA)", 175, 230, 350, 48,
                   lambda: setattr(self, "mode", GameMode.PVA),
                   selected=(self.mode == GameMode.PVA)),
            Button("AI vs AI (Spectate)", 175, 290, 350, 48,
                   lambda: setattr(self, "mode", GameMode.AVA),
                   selected=(self.mode == GameMode.AVA)),
            # AI Difficulty
            Button("AI: Easy (Heuristic)", 175, 370, 350, 44,
                   lambda: setattr(self, "ai_difficulty", AIDifficulty.EASY),
                   selected=(self.ai_difficulty == AIDifficulty.EASY)),
            Button("AI: Medium (Minimax D3)", 175, 424, 350, 44,
                   lambda: setattr(self, "ai_difficulty", AIDifficulty.MEDIUM),
                   selected=(self.ai_difficulty == AIDifficulty.MEDIUM)),
            Button("AI: Hard (Minimax D5)", 175, 478, 350, 44,
                   lambda: setattr(self, "ai_difficulty", AIDifficulty.HARD),
                   selected=(self.ai_difficulty == AIDifficulty.HARD)),
            Button("Back to Menu", 225, 550, 250, 50, lambda: self._set_state("MENU"), color=RED),
        ]

        for btn in buttons:
            btn.draw(self.screen, self.font)

        pygame.display.flip()
        self.clock.tick(DEFAULT_FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            for btn in buttons:
                if btn.handle_event(event):
                    break
        return True

    def _run_theme_menu(self) -> bool:
        self.screen.fill(BLACK)
        title_surf = self.title_font.render("THEMES & CHIPS", True, WHITE)
        self.screen.blit(title_surf, title_surf.get_rect(center=(350, 90)))

        buttons = [
            Button("Classic: Red vs Yellow", 175, 200, 350, 50,
                   lambda: self._set_themes("red", "yellow"),
                   selected=(self.p1_theme == "red" and self.p2_theme == "yellow")),
            Button("Vibrant: Green vs Violet", 175, 270, 350, 50,
                   lambda: self._set_themes("green", "violet"),
                   selected=(self.p1_theme == "green" and self.p2_theme == "violet")),
            Button("Modern: Neon Blue vs Dark Blue", 175, 340, 350, 50,
                   lambda: self._set_themes("neonBlue", "darkBlue"),
                   selected=(self.p1_theme == "neonBlue" and self.p2_theme == "darkBlue")),
            Button("Monochrome: Red vs Gray", 175, 410, 350, 50,
                   lambda: self._set_themes("red", "gray"),
                   selected=(self.p1_theme == "red" and self.p2_theme == "gray")),
            Button("Back to Menu", 225, 510, 250, 50, lambda: self._set_state("MENU"), color=RED),
        ]

        for btn in buttons:
            btn.draw(self.screen, self.font)

        pygame.display.flip()
        self.clock.tick(DEFAULT_FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            for btn in buttons:
                if btn.handle_event(event):
                    break
        return True

    def _run_gameplay(self) -> bool:
        assert self.game is not None and self.renderer is not None

        winning_coords = None
        if self.game.winner:
            winning_coords = self.game.board.get_winning_coordinates(int(self.game.winner))

        self.renderer.draw_board(self.game, winning_coords=winning_coords)

        if self.game.is_game_over:
            self.renderer.draw_game_over(self.game)

        pygame.display.flip()
        self.clock.tick(DEFAULT_FPS)

        # AI Turn Handling
        if not self.game.is_game_over:
            current_agent = self.game.get_current_agent()
            if current_agent:
                # Add slight delay for human visibility
                pygame.time.wait(150)
                move = self.game.play_ai_turn()
                if move:
                    assets.play_sound("drop")
                return True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEMOTION:
                self.renderer.set_hover_pos(event.pos[0])

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game.is_game_over:
                    # Click resets or opens menu
                    self.game.restart()
                else:
                    col = int(math.floor(event.pos[0] / self.sq_size))
                    if self.game.board.is_valid_location(col):
                        move = self.game.make_move(col)
                        assets.play_sound("drop")
                        if move.is_win:
                            assets.play_sound("win")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Return to main menu
                    self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
                    self.state = "MENU"
                    return True
                elif event.key == pygame.K_r:
                    self.game.restart()
                elif event.key == pygame.K_z and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    self.game.undo()
                    if self.game.mode == GameMode.PVA:
                        self.game.undo()

        return True

    def _set_state(self, new_state: str) -> None:
        self.state = new_state

    def _set_dims(self, cols: int, rows: int, win: int) -> None:
        self.dimensions = BoardDimensions(cols=cols, rows=rows, win_condition=win)
        self.state = "MENU"

    def _set_themes(self, p1: str, p2: str) -> None:
        self.p1_theme = p1
        self.p2_theme = p2
        self.state = "MENU"


def run_gui() -> None:
    app = Connect4App()
    app.run()
