from __future__ import annotations

import math
import sys
from typing import Optional

import pygame
from pygame.gfxdraw import aacircle, filled_circle

from connect4.ai.factory import AgentFactory
from connect4.config import (
    AMBER,
    BLUE,
    CRIMSON,
    CYAN,
    DEFAULT_FPS,
    DEFAULT_SQ_SIZE,
    EMERALD,
    GRAY,
    GREEN,
    PURPLE,
    RED,
    SLATE_700,
    SLATE_850,
    SLATE_900,
    SLATE_950,
    WHITE,
)
from connect4.game import Connect4Game
from connect4.gui.assets import assets
from connect4.gui.menu import Button, FloatingDisc
from connect4.gui.renderer import GameRenderer
from connect4.types import AIDifficulty, BoardDimensions, GameMode


class Connect4App:
    """
    Main GUI application controller for Connect 4.
    Orchestrates screen transitions, user interactions, AI background turns,
    physics drop animations, and rendering cycles.
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
        self.screen_width = 720
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Typography
        font_name = "Helvetica" if "Helvetica" in pygame.font.get_fonts() else "monospace"
        self.font = pygame.font.SysFont(font_name, 22, bold=True)
        self.sub_font = pygame.font.SysFont(font_name, 16, bold=True)
        self.title_font = pygame.font.SysFont(font_name, 44, bold=True)

        self.state = "MENU"  # 'MENU', 'SIZE', 'MODE', 'THEME', 'PLAYING', 'GAME_OVER'
        self.game: Optional[Connect4Game] = None
        self.renderer: Optional[GameRenderer] = None

        # Ambient floating discs for menu background
        self.floating_discs = [
            FloatingDisc(self.screen_width, self.screen_height) for _ in range(9)
        ]

    def start_game(self) -> None:
        """Initializes a new gameplay session and sets up geometry."""
        agent1 = None
        agent2 = None

        if self.mode == GameMode.PVA:
            agent2 = AgentFactory.create_agent(
                self.ai_difficulty, name=f"AI ({self.ai_difficulty.value.title()})"
            )
        elif self.mode == GameMode.AVA:
            agent1 = AgentFactory.create_agent(AIDifficulty.HARD, name="AI P1 (Hard)")
            agent2 = AgentFactory.create_agent(
                self.ai_difficulty, name=f"AI P2 ({self.ai_difficulty.value.title()})"
            )

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

    def _draw_menu_backdrop(self, dt: float) -> None:
        """Draws ambient dark gradient and updates floating background discs."""
        for y in range(0, self.screen_height, 4):
            ratio = y / max(1, self.screen_height)
            r = int(SLATE_950[0] + (SLATE_900[0] - SLATE_950[0]) * ratio)
            g = int(SLATE_950[1] + (SLATE_900[1] - SLATE_950[1]) * ratio)
            b = int(SLATE_950[2] + (SLATE_900[2] - SLATE_950[2]) * ratio)
            pygame.draw.rect(self.screen, (r, g, b), (0, y, self.screen_width, 4))

        for disc in self.floating_discs:
            disc.update(dt)
            disc.draw(self.screen)

    def _run_main_menu(self) -> bool:
        dt = min(self.clock.tick(DEFAULT_FPS) / 1000.0, 0.05)
        self._draw_menu_backdrop(dt)

        # Title with drop shadow
        cx = self.screen_width // 2
        shadow_surf = self.title_font.render("CONNECT FOUR", True, SLATE_950)
        self.screen.blit(shadow_surf, shadow_surf.get_rect(center=(cx + 2, 82)))
        title_surf = self.title_font.render("CONNECT FOUR", True, WHITE)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 80)))

        sub_title = self.sub_font.render(
            "PRODUCTION EDITION  •  AI ENGINE & GAME SUITE", True, CYAN
        )
        self.screen.blit(sub_title, sub_title.get_rect(center=(cx, 125)))

        # Current configuration badge
        mode_label = (
            "P vs P"
            if self.mode == GameMode.PVP
            else ("P vs AI" if self.mode == GameMode.PVA else "AI vs AI")
        )
        diff_str = f" ({self.ai_difficulty.value.title()})" if self.mode != GameMode.PVP else ""
        cfg_str = f"{self.dimensions.cols}x{self.dimensions.rows} Board  |  Connect {self.dimensions.win_condition}  |  {mode_label}{diff_str}"
        cfg_surf = self.sub_font.render(cfg_str, True, AMBER)
        cfg_rect = cfg_surf.get_rect(center=(cx, 170))
        pill_rect = cfg_rect.inflate(28, 12)
        pygame.draw.rect(self.screen, SLATE_850, pill_rect, border_radius=14)
        pygame.draw.rect(self.screen, SLATE_700, pill_rect, width=1, border_radius=14)
        self.screen.blit(cfg_surf, cfg_rect)

        # Buttons
        btn_w = 380
        btn_x = (self.screen_width - btn_w) // 2
        buttons = [
            Button(
                "▶   START GAME",
                btn_x,
                225,
                btn_w,
                54,
                lambda: self.start_game(),
                color=EMERALD,
                hover_color=GREEN,
            ),
            Button("🎮   Game Mode & AI", btn_x, 298, btn_w, 50, lambda: self._set_state("MODE")),
            Button("📐   Board Dimensions", btn_x, 365, btn_w, 50, lambda: self._set_state("SIZE")),
            Button("🎨   Themes & Colors", btn_x, 432, btn_w, 50, lambda: self._set_state("THEME")),
            Button(
                "✕   QUIT GAME",
                btn_x + 60,
                525,
                btn_w - 120,
                48,
                lambda: sys.exit(0),
                color=CRIMSON,
                hover_color=RED,
            ),
        ]

        for btn in buttons:
            btn.draw(self.screen, self.font)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            for btn in buttons:
                if btn.handle_event(event):
                    break
        return True

    def _run_size_menu(self) -> bool:
        dt = min(self.clock.tick(DEFAULT_FPS) / 1000.0, 0.05)
        self._draw_menu_backdrop(dt)
        cx = self.screen_width // 2

        title_surf = self.title_font.render("BOARD DIMENSIONS", True, WHITE)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 90)))

        btn_w = 400
        btn_x = (self.screen_width - btn_w) // 2
        buttons = [
            Button(
                "Standard 7x6 (Connect 4)",
                btn_x,
                190,
                btn_w,
                52,
                lambda: self._set_dims(7, 6, 4),
                selected=(self.dimensions == BoardDimensions(7, 6, 4)),
            ),
            Button(
                "Mini 4x3 (Connect 3)",
                btn_x,
                260,
                btn_w,
                52,
                lambda: self._set_dims(4, 3, 3),
                selected=(self.dimensions == BoardDimensions(4, 3, 3)),
            ),
            Button(
                "Large 8x7 (Connect 4)",
                btn_x,
                330,
                btn_w,
                52,
                lambda: self._set_dims(8, 7, 4),
                selected=(self.dimensions == BoardDimensions(8, 7, 4)),
            ),
            Button(
                "Challenge 7x6 (Connect 5)",
                btn_x,
                400,
                btn_w,
                52,
                lambda: self._set_dims(7, 6, 5),
                selected=(self.dimensions == BoardDimensions(7, 6, 5)),
            ),
            Button(
                "← Back to Menu",
                btn_x + 75,
                495,
                btn_w - 150,
                48,
                lambda: self._set_state("MENU"),
                color=SLATE_700,
            ),
        ]

        for btn in buttons:
            btn.draw(self.screen, self.font)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            for btn in buttons:
                if btn.handle_event(event):
                    break
        return True

    def _run_mode_menu(self) -> bool:
        dt = min(self.clock.tick(DEFAULT_FPS) / 1000.0, 0.05)
        self._draw_menu_backdrop(dt)
        cx = self.screen_width // 2

        title_surf = self.title_font.render("MODE & DIFFICULTY", True, WHITE)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 75)))

        btn_w = 400
        btn_x = (self.screen_width - btn_w) // 2
        buttons = [
            Button(
                "Player vs Player (PvP)",
                btn_x,
                155,
                btn_w,
                48,
                lambda: setattr(self, "mode", GameMode.PVP),
                selected=(self.mode == GameMode.PVP),
            ),
            Button(
                "Player vs AI (PvA)",
                btn_x,
                215,
                btn_w,
                48,
                lambda: setattr(self, "mode", GameMode.PVA),
                selected=(self.mode == GameMode.PVA),
            ),
            Button(
                "AI vs AI (Spectate)",
                btn_x,
                275,
                btn_w,
                48,
                lambda: setattr(self, "mode", GameMode.AVA),
                selected=(self.mode == GameMode.AVA),
            ),
            # AI Difficulty Selectors
            Button(
                "AI: Easy (1-Ply Tactical)",
                btn_x,
                355,
                btn_w,
                44,
                lambda: setattr(self, "ai_difficulty", AIDifficulty.EASY),
                selected=(self.ai_difficulty == AIDifficulty.EASY),
            ),
            Button(
                "AI: Medium (Minimax D3)",
                btn_x,
                408,
                btn_w,
                44,
                lambda: setattr(self, "ai_difficulty", AIDifficulty.MEDIUM),
                selected=(self.ai_difficulty == AIDifficulty.MEDIUM),
            ),
            Button(
                "AI: Hard (Minimax D5 Alpha-Beta)",
                btn_x,
                461,
                btn_w,
                44,
                lambda: setattr(self, "ai_difficulty", AIDifficulty.HARD),
                selected=(self.ai_difficulty == AIDifficulty.HARD),
            ),
            Button(
                "← Back to Menu",
                btn_x + 75,
                545,
                btn_w - 150,
                48,
                lambda: self._set_state("MENU"),
                color=SLATE_700,
            ),
        ]

        for btn in buttons:
            btn.draw(self.screen, self.font)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            for btn in buttons:
                if btn.handle_event(event):
                    break
        return True

    def _run_theme_menu(self) -> bool:
        dt = min(self.clock.tick(DEFAULT_FPS) / 1000.0, 0.05)
        self._draw_menu_backdrop(dt)
        cx = self.screen_width // 2

        title_surf = self.title_font.render("THEMES & CHIPS", True, WHITE)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 80)))

        btn_w = 420
        btn_x = (self.screen_width - btn_w) // 2
        theme_options = [
            ("Classic: Ruby Red vs Golden Amber", "red", "yellow", CRIMSON, AMBER),
            ("Vibrant: Emerald Green vs Amethyst", "green", "violet", EMERALD, PURPLE),
            ("Modern: Electric Cyan vs Midnight", "neonBlue", "darkBlue", CYAN, BLUE),
            ("Monochrome: Ruby Red vs Silver Gray", "red", "gray", CRIMSON, GRAY),
        ]

        buttons = []
        y_pos = 180
        for title, t1, t2, c1, c2 in theme_options:
            is_active = self.p1_theme == t1 and self.p2_theme == t2
            btn = Button(
                title,
                btn_x,
                y_pos,
                btn_w,
                52,
                lambda t1=t1, t2=t2: self._set_themes(t1, t2),
                selected=is_active,
            )
            buttons.append((btn, c1, c2))
            y_pos += 68

        back_btn = Button(
            "← Back to Menu",
            btn_x + 85,
            490,
            btn_w - 170,
            48,
            lambda: self._set_state("MENU"),
            color=SLATE_700,
        )

        for btn, c1, c2 in buttons:
            btn.draw(self.screen, self.font)
            # Render circular preview swatch chips on the right edge of each button
            chip_r = 13
            swatch_x1 = btn.rect.right - 44
            swatch_x2 = btn.rect.right - 18
            swatch_y = btn.rect.centery
            # Anti-aliased circular preview swatch chips
            filled_circle(self.screen, swatch_x1, swatch_y, chip_r, c1)
            aacircle(self.screen, swatch_x1, swatch_y, chip_r, c1)
            filled_circle(self.screen, swatch_x2, swatch_y, chip_r, c2)
            aacircle(self.screen, swatch_x2, swatch_y, chip_r, c2)
            aacircle(self.screen, swatch_x1, swatch_y, chip_r, WHITE)
            aacircle(self.screen, swatch_x2, swatch_y, chip_r, WHITE)

        back_btn.draw(self.screen, self.font)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            for btn, _, _ in buttons:
                if btn.handle_event(event):
                    break
            back_btn.handle_event(event)
        return True

    def _run_gameplay(self) -> bool:
        assert self.game is not None and self.renderer is not None

        dt = min(self.clock.tick(DEFAULT_FPS) / 1000.0, 0.05)

        winning_coords = None
        if self.game.winner:
            winning_coords = self.game.board.get_winning_coordinates(int(self.game.winner))

        self.renderer.draw_board(self.game, winning_coords=winning_coords, dt=dt)

        if self.game.is_game_over:
            self.renderer.draw_game_over(self.game)

        pygame.display.flip()

        # Handle AI Turn (Wait until any active drop animations settle)
        if not self.game.is_game_over and not self.renderer.is_animating:
            current_agent = self.game.get_current_agent()
            if current_agent:
                pygame.time.wait(140)
                col = current_agent.get_move(self.game.board, int(self.game.current_player))
                if self.game.board.is_valid_location(col):
                    open_row = self.game.board.get_next_open_row(col)
                    self.renderer.trigger_drop_animation(col, open_row, self.game.current_player)
                    self.game.make_move(col)
                return True

        # Process user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEMOTION:
                self.renderer.set_hover_pos(event.pos[0])

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game.is_game_over:
                    # Click resets the game
                    self.game.restart()
                    self.renderer.celebration_started = False
                elif not self.renderer.is_animating:
                    # Only accept human clicks when it is human's turn
                    if self.game.get_current_agent() is None:
                        col = int(math.floor(event.pos[0] / self.sq_size))
                        if self.game.board.is_valid_location(col):
                            open_row = self.game.board.get_next_open_row(col)
                            self.renderer.trigger_drop_animation(
                                col, open_row, self.game.current_player
                            )
                            self.game.make_move(col)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Return to main menu
                    self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
                    self.state = "MENU"
                    return True
                elif event.key == pygame.K_r:
                    self.game.restart()
                    self.renderer.celebration_started = False
                elif event.key in (pygame.K_u, pygame.K_z):
                    self.game.undo()
                    if self.game.mode == GameMode.PVA:
                        self.game.undo()
                elif event.key == pygame.K_m:
                    assets.toggle_mute()
                elif event.key == pygame.K_t:
                    self._cycle_theme()

        return True

    def _cycle_theme(self) -> None:
        """Cycles chip color themes dynamically during gameplay."""
        theme_pairs = [
            ("red", "yellow"),
            ("green", "violet"),
            ("neonBlue", "darkBlue"),
            ("red", "gray"),
        ]
        curr = (self.p1_theme, self.p2_theme)
        idx = theme_pairs.index(curr) if curr in theme_pairs else -1
        next_pair = theme_pairs[(idx + 1) % len(theme_pairs)]
        self.p1_theme, self.p2_theme = next_pair
        if self.renderer:
            self.renderer.p1_theme = self.p1_theme
            self.renderer.p2_theme = self.p2_theme

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
