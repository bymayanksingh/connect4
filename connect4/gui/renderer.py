from __future__ import annotations

import math
import random
from typing import List, Optional, Set, Tuple

import pygame
from pygame.gfxdraw import aacircle, aapolygon, filled_circle, filled_polygon

from connect4.config import (
    AMBER,
    BOARD_BLUE_DARK,
    BOARD_BLUE_MID,
    BOARD_BLUE_RIM,
    BOARD_BLUE_TOP,
    COLOR_THEMES,
    CRIMSON,
    CYAN,
    DEFAULT_SQ_SIZE,
    EMERALD,
    GOLD,
    GRAY,
    SLATE_700,
    SLATE_900,
    SLATE_950,
    WHITE,
)
from connect4.game import Connect4Game
from connect4.gui.assets import assets
from connect4.types import GameStatus, Player


class ConsoleBuffer:
    """In-game terminal logs buffer for the GUI stats panel."""

    def __init__(self, max_lines: int = 500):
        self.lines: List[str] = []
        self.max_lines = max_lines

    def log(self, text: str) -> None:
        for line in str(text).splitlines():
            self.lines.append(line)
        if len(self.lines) > self.max_lines:
            self.lines = self.lines[-self.max_lines :]

    def clear(self) -> None:
        self.lines.clear()


class DropAnimation:
    """Physics-based falling coin animation with elastic micro-bounce."""

    def __init__(
        self,
        col: int,
        target_row: int,
        player: Player,
        color: Tuple[int, int, int],
        theme: str,
        start_x: float,
        start_y: float,
        target_y: float,
        gravity: float = 3400.0,
    ):
        self.col = col
        self.target_row = target_row
        self.player = player
        self.color = color
        self.theme = theme
        self.x = start_x
        self.y = start_y
        self.target_y = target_y
        self.vy = 0.0
        self.gravity = gravity
        self.bounce_count = 0
        self.max_bounces = 2
        self.is_finished = False

    def update(self, dt: float) -> bool:
        """Advances physics. Returns True if settled, False if animating."""
        if self.is_finished:
            return True

        self.vy += self.gravity * dt
        self.y += self.vy * dt

        if self.y >= self.target_y:
            self.y = self.target_y
            if self.bounce_count < self.max_bounces and abs(self.vy) > 160:
                self.vy = -self.vy * 0.28
                self.bounce_count += 1
                assets.play_sound("drop")
            else:
                self.vy = 0.0
                self.is_finished = True
                assets.play_sound("drop")
        return self.is_finished


class ConfettiParticle:
    """Celebratory particle fluttering across screen on win."""

    def __init__(self, x: float, y: float, colors: List[Tuple[int, int, int]]):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(120, 480)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed - random.uniform(100, 300)
        self.color = random.choice(colors)
        self.size = random.uniform(4, 9)
        self.rot = random.uniform(0, 360)
        self.v_rot = random.uniform(-360, 360)
        self.life = random.uniform(2.5, 4.5)
        self.max_life = self.life

    def update(self, dt: float) -> bool:
        self.x += self.vx * dt
        self.vy += (500 + random.uniform(-20, 20)) * dt  # Gravity
        self.vx *= 0.985  # Drag
        self.rot += self.v_rot * dt
        self.life -= dt
        return self.life > 0

    def draw(self, screen: pygame.Surface) -> None:
        if self.life <= 0:
            return
        alpha = int(255 * (self.life / self.max_life))
        rad = max(1, int(self.size))
        surf = pygame.Surface((rad * 2, rad * 2), pygame.SRCALPHA)
        color_rgba = (self.color[0], self.color[1], self.color[2], min(255, alpha))
        pygame.draw.rect(surf, color_rgba, (0, 0, rad * 2, rad * 2), border_radius=2)
        screen.blit(surf, (int(self.x - rad), int(self.y - rad)))


class GameRenderer:
    """
    Production-grade visual renderer for Connect 4.
    Features:
    - High-definition 3D acrylic chips with specular studio gloss.
    - Deep metallic blue board casing with transparent slot cutouts.
    - Physics-based coin drop gravity animation with micro-bounce.
    - Dynamic top HUD with active turn breathing glow.
    - Interactive column hover beam & floating preview piece.
    - Pulsing golden winning line laser & confetti particle explosion.
    - Responsive bottom action dock and diagnostic stats console.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        sq_size: int = DEFAULT_SQ_SIZE,
        p1_theme: str = "red",
        p2_theme: str = "yellow",
        board_color: Tuple[int, int, int] = BOARD_BLUE_MID,
        show_console: bool = False,
    ):
        self.screen = screen
        self.sq_size = sq_size
        self.radius = int(sq_size / 2 - 6)
        self.p1_theme = p1_theme
        self.p2_theme = p2_theme
        self.board_color = board_color
        self.show_console = show_console
        self.console = ConsoleBuffer()

        self.hover_x: Optional[int] = None
        self.time_elapsed: float = 0.0
        self.active_drops: List[DropAnimation] = []
        self.particles: List[ConfettiParticle] = []
        self.celebration_started: bool = False

        self._board_surface_cache: Optional[pygame.Surface] = None
        self._well_surface_cache: Optional[pygame.Surface] = None
        self._cached_dims: Optional[Tuple[int, int, int]] = None
        self._init_fonts()

    def _init_fonts(self) -> None:
        if not pygame.font.get_init():
            pygame.font.init()
        font_name = "Helvetica" if "Helvetica" in pygame.font.get_fonts() else "monospace"
        self.title_font = pygame.font.SysFont(
            font_name, max(18, int(self.sq_size * 0.38)), bold=True
        )
        self.hud_font = pygame.font.SysFont(font_name, max(14, int(self.sq_size * 0.22)), bold=True)
        self.small_font = pygame.font.SysFont(
            font_name, max(11, int(self.sq_size * 0.16)), bold=True
        )
        self.console_font = pygame.font.SysFont("monospace", 13)

    def get_p1_color(self) -> Tuple[int, int, int]:
        return COLOR_THEMES.get(self.p1_theme, (CRIMSON, ""))[0]

    def get_p2_color(self) -> Tuple[int, int, int]:
        return COLOR_THEMES.get(self.p2_theme, (AMBER, ""))[0]

    def set_hover_pos(self, mouse_x: int) -> None:
        self.hover_x = mouse_x

    def trigger_drop_animation(self, col: int, target_row: int, player: Player) -> None:
        """Queues a physics-based coin drop animation."""
        color = self.get_p1_color() if player == Player.P1 else self.get_p2_color()
        theme = self.p1_theme if player == Player.P1 else self.p2_theme
        cx = col * self.sq_size + self.sq_size // 2
        start_y = float(self.sq_size // 2)
        # Visual row index: 0 is top grid row, (rows - 1 - target_row) is vertical position
        target_visual_r = 6 - 1 - target_row  # Default standard rows; dynamic in update
        target_y = float((target_visual_r + 1) * self.sq_size + self.sq_size // 2)

        anim = DropAnimation(
            col=col,
            target_row=target_row,
            player=player,
            color=color,
            theme=theme,
            start_x=float(cx),
            start_y=start_y,
            target_y=target_y,
        )
        self.active_drops.append(anim)

    def trigger_win_celebration(
        self, winning_coords: List[Tuple[int, int]], board_cols: int
    ) -> None:
        """Launches a festive confetti particle explosion around winning chips."""
        if not winning_coords:
            return
        colors = [
            self.get_p1_color(),
            self.get_p2_color(),
            GOLD,
            WHITE,
            CYAN,
            EMERALD,
        ]
        self.particles.clear()
        for r, c in winning_coords:
            cx = c * self.sq_size + self.sq_size // 2
            cy = (6 - 1 - r + 1) * self.sq_size + self.sq_size // 2
            for _ in range(25):
                self.particles.append(ConfettiParticle(cx, cy, colors))
        self.celebration_started = True
        assets.play_sound("win")

    def update(self, dt: float = 0.016, total_rows: int = 6) -> None:
        """Advances physics, particle lifespans, and lighting phases."""
        self.time_elapsed += dt

        # Update drop animations
        for drop in self.active_drops:
            # Correct target_y with exact total rows if known
            visual_r = total_rows - 1 - drop.target_row
            drop.target_y = float((visual_r + 1) * self.sq_size + self.sq_size // 2)
            drop.update(dt)
        self.active_drops = [d for d in self.active_drops if not d.is_finished]

        # Update confetti particles
        self.particles = [p for p in self.particles if p.update(dt)]

    @property
    def is_animating(self) -> bool:
        return len(self.active_drops) > 0

    def _get_well_surface(self) -> pygame.Surface:
        """Cached 2x supersampled empty slot well with smooth inner ambient occlusion."""
        if self._well_surface_cache is not None:
            return self._well_surface_cache

        scale = 2
        hi_r = self.radius * scale
        hi_size = hi_r * 2
        hi_surf = pygame.Surface((hi_size, hi_size), pygame.SRCALPHA)

        # Deep dark backdrop well
        filled_circle(hi_surf, hi_r, hi_r, hi_r - 2, SLATE_950)
        aacircle(hi_surf, hi_r, hi_r, hi_r - 2, SLATE_950)

        # Smooth inner upper recessed shadow arc
        rect = pygame.Rect(0, 0, hi_size, hi_size)
        pygame.draw.arc(hi_surf, (5, 8, 14, 230), rect, 0.15, 3.0, 6)
        # Smooth lower subtle highlight arc
        pygame.draw.arc(hi_surf, (30, 58, 138, 180), rect, 3.4, 6.0, 4)

        self._well_surface_cache = pygame.transform.smoothscale(
            hi_surf, (self.radius * 2, self.radius * 2)
        )
        return self._well_surface_cache

    def _draw_aa_capsule_line(
        self,
        surf: pygame.Surface,
        p1: Tuple[float, float],
        p2: Tuple[float, float],
        color: Tuple[int, int, int],
        width: float,
    ) -> None:
        """Renders an anti-aliased thick line segment with rounded end caps."""
        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        half_w = width / 2.0
        nx = -dy / dist * half_w
        ny = dx / dist * half_w
        pts = [
            (int(round(x1 + nx)), int(round(y1 + ny))),
            (int(round(x2 + nx)), int(round(y2 + ny))),
            (int(round(x2 - nx)), int(round(y2 - ny))),
            (int(round(x1 - nx)), int(round(y1 - ny))),
        ]
        filled_polygon(surf, pts, color)
        aapolygon(surf, pts, color)
        cap_r = int(round(half_w))
        if cap_r >= 1:
            filled_circle(surf, int(round(x1)), int(round(y1)), cap_r, color)
            aacircle(surf, int(round(x1)), int(round(y1)), cap_r, color)
            filled_circle(surf, int(round(x2)), int(round(y2)), cap_r, color)
            aacircle(surf, int(round(x2)), int(round(y2)), cap_r, color)

    def _get_board_surface(self, cols: int, rows: int) -> pygame.Surface:
        """Generates or retrieves cached front blue board plate with transparent hole cutouts."""
        cache_key = (cols, rows, self.sq_size)
        if self._board_surface_cache is not None and self._cached_dims == cache_key:
            return self._board_surface_cache

        board_w = cols * self.sq_size
        board_h = rows * self.sq_size
        board_surf = pygame.Surface((board_w, board_h), pygame.SRCALPHA)

        # 1. Fill with metallic royal blue vertical gradient
        for y in range(board_h):
            ratio = y / max(1, board_h)
            br = int(BOARD_BLUE_TOP[0] * (1 - ratio * 0.22) + BOARD_BLUE_DARK[0] * (ratio * 0.22))
            bg = int(BOARD_BLUE_TOP[1] * (1 - ratio * 0.20) + BOARD_BLUE_DARK[1] * (ratio * 0.20))
            bb = int(BOARD_BLUE_TOP[2] * (1 - ratio * 0.18) + BOARD_BLUE_DARK[2] * (ratio * 0.18))
            pygame.draw.line(board_surf, (br, bg, bb, 255), (0, y), (board_w, y))

        # 2. Beveled rounded outer border
        pygame.draw.rect(
            board_surf, BOARD_BLUE_RIM, (0, 0, board_w, board_h), width=2, border_radius=14
        )

        # 3. Transparent hole cutout cutter generated with 4x supersampling (SSAA)
        scale = 4
        hi_radius = self.radius * scale
        hi_size = hi_radius * 2
        hi_cutter = pygame.Surface((hi_size, hi_size), pygame.SRCALPHA)
        # Using RGB=(0, 0, 0, 255) ensures pure alpha subtraction with zero color contamination
        pygame.draw.circle(hi_cutter, (0, 0, 0, 255), (hi_radius, hi_radius), hi_radius)
        cutter = pygame.transform.smoothscale(hi_cutter, (self.radius * 2, self.radius * 2))

        for c in range(cols):
            for r in range(rows):
                cx = c * self.sq_size + self.sq_size // 2
                cy = r * self.sq_size + self.sq_size // 2
                board_surf.blit(
                    cutter,
                    (cx - self.radius, cy - self.radius),
                    special_flags=pygame.BLEND_RGBA_SUB,
                )
                # Delicate anti-aliased bevel rim around each hole opening
                aacircle(board_surf, cx, cy, self.radius, (45, 80, 185))

        self._board_surface_cache = board_surf
        self._cached_dims = cache_key
        return board_surf

    def draw_board(
        self,
        game: Connect4Game,
        winning_coords: Optional[List[Tuple[int, int]]] = None,
        dt: float = 0.016,
    ) -> None:
        """Main frame rendering method. Draws all visual layers seamlessly."""
        self.update(dt=dt, total_rows=game.board.rows)

        board = game.board
        cols, rows = board.cols, board.rows
        width = cols * self.sq_size
        height = (rows + 1) * self.sq_size

        # Layer 1: Dark ambient slate background
        for y in range(0, height, 4):
            ratio = y / max(1, height)
            r = int(SLATE_950[0] + (SLATE_900[0] - SLATE_950[0]) * ratio)
            g = int(SLATE_950[1] + (SLATE_900[1] - SLATE_950[1]) * ratio)
            b = int(SLATE_950[2] + (SLATE_900[2] - SLATE_950[2]) * ratio)
            pygame.draw.rect(self.screen, (r, g, b), (0, y, width, 4))

        # Check celebration trigger
        if game.is_game_over and game.winner and not self.celebration_started and winning_coords:
            self.trigger_win_celebration(winning_coords, cols)

        # Layer 2: Empty slot recessed hole depth (ambient inner shadows)
        well_surf = self._get_well_surface()
        for c in range(cols):
            for r in range(rows):
                cx = c * self.sq_size + self.sq_size // 2
                cy = (r + 1) * self.sq_size + self.sq_size // 2
                self.screen.blit(well_surf, (cx - self.radius, cy - self.radius))

        # Layer 3: Placed Discs & Active Falling Drops (rendered behind front plate)
        # Set of drop positions to avoid double-drawing during physics animation
        animating_cells: Set[Tuple[int, int]] = {(d.target_row, d.col) for d in self.active_drops}

        for c in range(cols):
            for r in range(rows):
                cell_val = board.board[r][c]
                if cell_val == 0 or (r, c) in animating_cells:
                    continue
                visual_r = rows - 1 - r
                cx = c * self.sq_size + self.sq_size // 2
                cy = (visual_r + 1) * self.sq_size + self.sq_size // 2

                if cell_val == 1:
                    chip = assets.get_coin_surface(self.get_p1_color(), self.radius, self.p1_theme)
                else:
                    chip = assets.get_coin_surface(self.get_p2_color(), self.radius, self.p2_theme)
                self.screen.blit(chip, (cx - self.radius, cy - self.radius))

        # Draw active drop animations
        for drop in self.active_drops:
            chip = assets.get_coin_surface(drop.color, self.radius, drop.theme)
            self.screen.blit(chip, (int(drop.x - self.radius), int(drop.y - self.radius)))

        # Layer 4: Front Blue Board Plate (with circular cutouts)
        board_surf = self._get_board_surface(cols, rows)
        self.screen.blit(board_surf, (0, self.sq_size))

        # Board table stands / feet
        foot_w = int(self.sq_size * 0.45)
        foot_h = 10
        pygame.draw.rect(
            self.screen,
            (20, 45, 110),
            (int(self.sq_size * 0.2), height - 6, foot_w, foot_h),
            border_radius=3,
        )
        pygame.draw.rect(
            self.screen,
            (20, 45, 110),
            (width - int(self.sq_size * 0.2) - foot_w, height - 6, foot_w, foot_h),
            border_radius=3,
        )

        # Layer 5: Interactive Hover Column Beam & Floating Piece
        if not game.is_game_over and self.hover_x is not None:
            clamped_x = max(0, min(self.hover_x, width - 1))
            hover_col = clamped_x // self.sq_size
            is_valid_col = board.is_valid_location(hover_col)

            # Translucent vertical light beam over target column
            beam_x = hover_col * self.sq_size
            beam_surf = pygame.Surface((self.sq_size, rows * self.sq_size), pygame.SRCALPHA)
            beam_color = (255, 255, 255, 16) if is_valid_col else (239, 68, 68, 25)
            beam_surf.fill(beam_color)
            self.screen.blit(beam_surf, (beam_x, self.sq_size))

            # Floating hover piece above the column
            chip_cx = hover_col * self.sq_size + self.sq_size // 2
            bob_offset = math.sin(self.time_elapsed * 5.0) * 3.0
            chip_cy = float(self.sq_size // 2) + bob_offset

            hover_color = (
                self.get_p1_color() if game.current_player == Player.P1 else self.get_p2_color()
            )
            hover_theme = self.p1_theme if game.current_player == Player.P1 else self.p2_theme
            hover_chip = assets.get_coin_surface(hover_color, self.radius, hover_theme)

            if is_valid_col:
                self.screen.blit(
                    hover_chip, (int(chip_cx - self.radius), int(chip_cy - self.radius))
                )
                # Subtle indicator chevron arrow pointing down (Anti-aliased)
                arrow_y = int(self.sq_size - 14 + math.sin(self.time_elapsed * 6.0) * 2.0)
                pts = [(chip_cx - 6, arrow_y), (chip_cx + 6, arrow_y), (chip_cx, arrow_y + 6)]
                filled_polygon(self.screen, pts, WHITE)
                aapolygon(self.screen, pts, WHITE)
            else:
                # Dimmed chip with full column indicator
                dimmed = hover_chip.copy()
                dimmed.set_alpha(100)
                self.screen.blit(dimmed, (int(chip_cx - self.radius), int(chip_cy - self.radius)))
                full_txt = self.small_font.render("FULL", True, CRIMSON)
                self.screen.blit(full_txt, full_txt.get_rect(center=(chip_cx, chip_cy)))

        # Layer 6: Winning Line Glowing Laser & Pulsing Halo
        if winning_coords:
            set(winning_coords)
            pulse = math.sin(self.time_elapsed * 7.0)
            halo_r = int(self.radius + 3 + pulse * 3)

            # Pulsing golden halos on winning chips (2x supersampled anti-aliasing)
            for r, c in winning_coords:
                visual_r = rows - 1 - r
                cx = c * self.sq_size + self.sq_size // 2
                cy = (visual_r + 1) * self.sq_size + self.sq_size // 2

                # Anti-aliased 2x supersampled halo ring
                scale = 2
                hi_halo_r = halo_r * scale
                hi_size = (halo_r * 2 + 8) * scale
                hi_halo = pygame.Surface((hi_size, hi_size), pygame.SRCALPHA)
                pygame.draw.circle(
                    hi_halo,
                    (251, 191, 36, int(180 + pulse * 60)),
                    (hi_size // 2, hi_size // 2),
                    hi_halo_r,
                    width=4 * scale,
                )
                halo_surf = pygame.transform.smoothscale(hi_halo, (halo_r * 2 + 8, halo_r * 2 + 8))
                self.screen.blit(halo_surf, (cx - halo_r - 4, cy - halo_r - 4))

                # Center golden star highlight
                star_surf = self.hud_font.render("★", True, WHITE)
                self.screen.blit(star_surf, star_surf.get_rect(center=(cx, cy)))

            # Anti-aliased laser beam connecting winning sequence
            if len(winning_coords) >= 2:
                # Sort coordinates to trace clean path
                sorted_coords = sorted(winning_coords)
                pts = [
                    (
                        float(c * self.sq_size + self.sq_size // 2),
                        float((rows - 1 - r + 1) * self.sq_size + self.sq_size // 2),
                    )
                    for r, c in sorted_coords
                ]
                for i in range(len(pts) - 1):
                    # Outer gold laser beam
                    self._draw_aa_capsule_line(self.screen, pts[i], pts[i + 1], GOLD, 8.0)
                    # Inner brilliant white core
                    self._draw_aa_capsule_line(self.screen, pts[i], pts[i + 1], WHITE, 3.5)

        # Layer 7: Confetti Particles
        for particle in self.particles:
            particle.draw(self.screen)

        # Layer 8: Modern Top HUD Banner
        self._draw_hud(game, width)

        # Layer 9: Console Panel if toggled
        if self.show_console:
            self._draw_console(width, height)

    def _draw_hud(self, game: Connect4Game, width: int) -> None:
        """Renders elegant glassmorphic top header with player cards and match status."""
        hud_h = int(self.sq_size * 0.88)
        hud_rect = pygame.Rect(10, 8, width - 20, hud_h)

        # Glassmorphic backdrop container
        glass = pygame.Surface((hud_rect.width, hud_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(
            glass, (20, 29, 47, 215), (0, 0, hud_rect.width, hud_rect.height), border_radius=12
        )
        pygame.draw.rect(
            glass,
            (51, 65, 85, 230),
            (0, 0, hud_rect.width, hud_rect.height),
            width=1,
            border_radius=12,
        )
        self.screen.blit(glass, hud_rect.topleft)

        # Player 1 Badge (Left) - Anti-aliased
        p1_active = game.current_player == Player.P1 and not game.is_game_over
        p1_cx = hud_rect.left + 32
        p1_cy = hud_rect.centery
        p1_color = self.get_p1_color()

        if p1_active:
            pulse = int(4 + math.sin(self.time_elapsed * 8.0) * 2)
            aacircle(self.screen, p1_cx, p1_cy, 18 + pulse, EMERALD)
            aacircle(self.screen, p1_cx, p1_cy, 17 + pulse, EMERALD)
        filled_circle(self.screen, p1_cx, p1_cy, 14, p1_color)
        aacircle(self.screen, p1_cx, p1_cy, 14, p1_color)
        p1_label = self.hud_font.render("PLAYER 1", True, WHITE if p1_active else GRAY)
        self.screen.blit(p1_label, (p1_cx + 20, p1_cy - 9))

        # Player 2 Badge (Right) - Anti-aliased
        p2_active = game.current_player == Player.P2 and not game.is_game_over
        p2_cx = hud_rect.right - 32
        p2_cy = hud_rect.centery
        p2_color = self.get_p2_color()

        if p2_active:
            pulse = int(4 + math.sin(self.time_elapsed * 8.0) * 2)
            aacircle(self.screen, p2_cx, p2_cy, 18 + pulse, EMERALD)
            aacircle(self.screen, p2_cx, p2_cy, 17 + pulse, EMERALD)
        filled_circle(self.screen, p2_cx, p2_cy, 14, p2_color)
        aacircle(self.screen, p2_cx, p2_cy, 14, p2_color)
        p2_name = "AI AGENT" if game.agent2 else "PLAYER 2"
        p2_label = self.hud_font.render(p2_name, True, WHITE if p2_active else GRAY)
        self.screen.blit(p2_label, (p2_cx - 20 - p2_label.get_width(), p2_cy - 9))

        # Center Status Pill
        if game.is_game_over:
            if game.status == GameStatus.DRAW:
                status_text = "🤝 MATCH DRAW"
                status_color = WHITE
            elif game.winner == Player.P1:
                status_text = "🏆 PLAYER 1 WINS!"
                status_color = p1_color
            else:
                status_text = f"🏆 {p2_name} WINS!"
                status_color = p2_color
        else:
            current_agent = game.get_current_agent()
            if current_agent:
                status_text = f"🤖 {current_agent.name} thinking..."
                status_color = AMBER
            else:
                status_text = "YOUR TURN" if game.current_player == Player.P1 else "PLAYER 2 TURN"
                status_color = WHITE

        status_surf = self.hud_font.render(status_text, True, status_color)
        status_rect = status_surf.get_rect(center=(hud_rect.centerx, hud_rect.centery))
        # Center pill background
        pill_rect = status_rect.inflate(24, 10)
        pygame.draw.rect(self.screen, SLATE_950, pill_rect, border_radius=14)
        pygame.draw.rect(self.screen, SLATE_700, pill_rect, width=1, border_radius=14)
        self.screen.blit(status_surf, status_rect)

    def draw_game_over(self, game: Connect4Game) -> None:
        """Draws a refined glassmorphic victory celebration modal."""
        width = game.board.cols * self.sq_size
        height = (game.board.rows + 1) * self.sq_size

        modal_w = min(460, width - 40)
        modal_h = 160
        modal_rect = pygame.Rect((width - modal_w) // 2, (height - modal_h) // 2, modal_w, modal_h)

        # Translucent dark backdrop card
        card_surf = pygame.Surface((modal_w, modal_h), pygame.SRCALPHA)
        pygame.draw.rect(card_surf, (15, 23, 42, 245), (0, 0, modal_w, modal_h), border_radius=18)
        pygame.draw.rect(
            card_surf, (59, 130, 246, 220), (0, 0, modal_w, modal_h), width=2, border_radius=18
        )
        self.screen.blit(card_surf, modal_rect.topleft)

        # Winner title
        if game.status == GameStatus.DRAW:
            msg = "IT'S A DRAW!"
            color = WHITE
            sub = "Well played by both sides!"
        elif game.status == GameStatus.WIN_P1:
            msg = "PLAYER 1 WINS!"
            color = self.get_p1_color()
            sub = f"Victory in {len(game.move_history)} moves!"
        else:
            winner_str = "AI AGENT WINS!" if game.agent2 else "PLAYER 2 WINS!"
            msg = winner_str
            color = self.get_p2_color()
            sub = f"Victory in {len(game.move_history)} moves!"

        title_surf = self.title_font.render(msg, True, color)
        self.screen.blit(
            title_surf, title_surf.get_rect(center=(modal_rect.centerx, modal_rect.top + 45))
        )

        sub_surf = self.hud_font.render(sub, True, WHITE)
        self.screen.blit(
            sub_surf, sub_surf.get_rect(center=(modal_rect.centerx, modal_rect.top + 85))
        )

        prompt_surf = self.small_font.render(
            "Press [R] to Play Again   •   [ESC] Main Menu", True, AMBER
        )
        self.screen.blit(
            prompt_surf, prompt_surf.get_rect(center=(modal_rect.centerx, modal_rect.top + 125))
        )

    def _draw_console(self, board_width: int, board_height: int) -> None:
        console_width = 300
        console_rect = pygame.Rect(board_width, 0, console_width, board_height)
        pygame.draw.rect(self.screen, SLATE_900, console_rect)
        pygame.draw.line(self.screen, SLATE_700, (board_width, 0), (board_width, board_height), 2)

        hdr = self.console_font.render("AGENT DIAGNOSTICS", True, GOLD)
        self.screen.blit(hdr, (board_width + 12, 12))

        y_offset = 38
        visible_lines = self.console.lines[-25:]
        for line in visible_lines:
            text_surf = self.console_font.render(line[:36], True, WHITE)
            self.screen.blit(text_surf, (board_width + 12, y_offset))
            y_offset += 18
