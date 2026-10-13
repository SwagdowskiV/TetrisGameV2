import array
import math
import random

import pygame

from board import BOARD_HEIGHT, BOARD_WIDTH, CELL_SIZE


WIDTH = 800
HEIGHT = 700
BOARD_X = 150
BOARD_Y = 50


class Graphics:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tetris")
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.SysFont("arial", 86, bold=True)
        self.menu_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 25)
        self.score_font = pygame.font.Font(None, 54)
        self.play_button = pygame.Rect(280, 320, 240, 64)
        self.shop_button = pygame.Rect(280, 408, 240, 64)
        self.settings_button = pygame.Rect(280, 496, 240, 64)

        self.background = self._create_background()
        self.menu_block_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.line_clear_effect_layer = pygame.Surface(
            (WIDTH, HEIGHT), pygame.SRCALPHA
        )
        self.menu_blocks = self._create_menu_blocks()
        self.line_clear_effects = []
        self.line_clear_sound = self._create_line_clear_sound()

    @staticmethod
    def _create_background():
        background = pygame.Surface((WIDTH, HEIGHT))
        for y in range(HEIGHT):
            amount = y / HEIGHT
            color = (
                int(17 + 34 * amount),
                int(10 + 12 * amount),
                int(43 + 59 * amount),
            )
            pygame.draw.line(background, color, (0, y), (WIDTH, y))
        return background

    @staticmethod
    def _create_menu_blocks():
        colors = ((112, 75, 210), (72, 116, 224), (0, 190, 205), (166, 91, 220))
        return [
            {
                "x": random.randint(20, WIDTH - 70),
                "y": random.randint(-HEIGHT, HEIGHT),
                "size": random.randint(18, 34),
                "speed": random.uniform(24, 65),
                "depth": random.randint(6, 12),
                "color": random.choice(colors),
                "alpha": random.randint(75, 145),
            }
            for _ in range(17)
        ]

    @staticmethod
    def _create_line_clear_sound():
        if pygame.mixer.get_init() is None:
            try:
                pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
            except pygame.error as error:
                print(f"Line-clear sound unavailable: {error}")
                return None

        mixer_settings = pygame.mixer.get_init()
        if mixer_settings is None:
            return None

        sample_rate, sample_size, channel_count = mixer_settings
        if sample_size != -16:
            print("Line-clear sound unavailable: mixer must use 16-bit audio.")
            return None

        samples = array.array("h")
        duration = 0.24
        for index in range(int(sample_rate * duration)):
            progress = index / sample_rate
            envelope = min(progress / 0.015, 1) * max(1 - progress / duration, 0)
            pitch = 740 + 360 * progress / duration
            tone = math.sin(2 * math.pi * pitch * progress)
            overtone = math.sin(2 * math.pi * pitch * 1.5 * progress)
            value = int(10000 * envelope * (tone * 0.72 + overtone * 0.28))
            for _ in range(channel_count):
                samples.append(value)
        return pygame.mixer.Sound(buffer=samples.tobytes())

    def reset_effects(self):
        self.line_clear_effects.clear()

    def _update_menu_blocks(self, delta_time):
        for block in self.menu_blocks:
            block["y"] += block["speed"] * delta_time
            if block["y"] - block["depth"] > HEIGHT:
                block["y"] = -block["size"] - block["depth"]
                block["x"] = random.randint(
                    20, WIDTH - block["size"] - block["depth"] - 10
                )

    @staticmethod
    def _draw_cube(surface, x, y, size, depth, color, alpha):
        front = pygame.Rect(x, y, size, size)
        top = (
            (x, y),
            (x + depth, y - depth // 2),
            (x + size + depth, y - depth // 2),
            (x + size, y),
        )
        side = (
            (x + size, y),
            (x + size + depth, y - depth // 2),
            (x + size + depth, y + size - depth // 2),
            (x + size, y + size),
        )
        lighter = tuple(min(channel + 55, 255) for channel in color)
        darker = tuple(max(channel - 45, 0) for channel in color)
        pygame.draw.polygon(surface, (*lighter, alpha), top)
        pygame.draw.polygon(surface, (*darker, alpha), side)
        pygame.draw.rect(surface, (*color, alpha), front)
        pygame.draw.line(
            surface,
            (*lighter, alpha),
            (x + 2, y + 2),
            (x + size - 2, y + 2),
            2,
        )
        pygame.draw.line(
            surface,
            (*darker, alpha),
            (x + size - 2, y + 3),
            (x + size - 2, y + size - 2),
            2,
        )

    def _draw_ambient_background(self, delta_time):
        self._update_menu_blocks(delta_time)
        self.screen.blit(self.background, (0, 0))
        self.menu_block_layer.fill((0, 0, 0, 0))
        for block in self.menu_blocks:
            self._draw_cube(
                self.menu_block_layer,
                int(block["x"]),
                int(block["y"]),
                block["size"],
                block["depth"],
                block["color"],
                block["alpha"],
            )
        self.screen.blit(self.menu_block_layer, (0, 0))

    def draw_menu(self, delta_time):
        self._draw_ambient_background(delta_time)
        title = self.title_font.render("TETRIS", True, (0, 220, 220))
        title_rect = title.get_rect(center=(WIDTH // 2, 190))
        for offset in range(8, 0, -1):
            extrusion = self.title_font.render(
                "TETRIS",
                True,
                (0, 63 + offset * 5, 92 + offset * 5),
            )
            self.screen.blit(extrusion, title_rect.move(offset, offset))
        self.screen.blit(title, title_rect)

        buttons = (
            (self.play_button, "PLAY", True),
            (self.shop_button, "SHOP", False),
            (self.settings_button, "SETTINGS", False),
        )
        for button, label, enabled in buttons:
            background = (25, 37, 61) if enabled else (22, 26, 39)
            foreground = (255, 255, 255) if enabled else (125, 132, 148)
            border = (0, 220, 220) if enabled else (65, 72, 89)
            pygame.draw.rect(self.screen, background, button, border_radius=10)
            pygame.draw.rect(self.screen, border, button, width=2, border_radius=10)
            label_surface = self.menu_font.render(label, True, foreground)
            self.screen.blit(label_surface, label_surface.get_rect(center=button.center))

        hint = self.small_font.render(
            "Press ENTER to play  |  Shop and Settings coming soon",
            True,
            (155, 166, 188),
        )
        self.screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 602)))

    def _draw_beveled_block(self, x, y, size, color):
        tile = pygame.Rect(x + 2, y + 2, size - 4, size - 4)
        lighter = tuple(min(channel + 55, 255) for channel in color)
        darker = tuple(max(channel - 65, 0) for channel in color)

        pygame.draw.rect(self.screen, (12, 8, 28), tile.move(2, 3), border_radius=3)
        pygame.draw.rect(self.screen, color, tile, border_radius=3)
        pygame.draw.line(
            self.screen,
            lighter,
            (tile.left + 3, tile.top + 2),
            (tile.right - 3, tile.top + 2),
            2,
        )
        pygame.draw.line(
            self.screen,
            lighter,
            (tile.left + 2, tile.top + 3),
            (tile.left + 2, tile.bottom - 3),
            2,
        )
        pygame.draw.line(
            self.screen,
            darker,
            (tile.left + 3, tile.bottom - 2),
            (tile.right - 2, tile.bottom - 2),
            2,
        )
        pygame.draw.line(
            self.screen,
            darker,
            (tile.right - 2, tile.top + 3),
            (tile.right - 2, tile.bottom - 3),
            2,
        )

    def _draw_board(self, landed_blocks, piece, piece_color):
        board_rect = pygame.Rect(
            BOARD_X - 12,
            BOARD_Y - 12,
            BOARD_WIDTH * CELL_SIZE + 24,
            BOARD_HEIGHT * CELL_SIZE + 24,
        )
        pygame.draw.rect(self.screen, (13, 8, 30), board_rect.move(8, 9), border_radius=12)
        pygame.draw.rect(self.screen, (40, 28, 75), board_rect, border_radius=12)
        pygame.draw.rect(
            self.screen, (126, 92, 198), board_rect, width=2, border_radius=12
        )

        grid_rect = pygame.Rect(
            BOARD_X,
            BOARD_Y,
            BOARD_WIDTH * CELL_SIZE,
            BOARD_HEIGHT * CELL_SIZE,
        )
        pygame.draw.rect(self.screen, (22, 16, 43), grid_rect)
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                x = BOARD_X + col * CELL_SIZE
                y = BOARD_Y + row * CELL_SIZE
                pygame.draw.rect(
                    self.screen, (51, 42, 76), (x, y, CELL_SIZE, CELL_SIZE), 1
                )

        for col, row, color in landed_blocks:
            self._draw_beveled_block(
                BOARD_X + col * CELL_SIZE,
                BOARD_Y + row * CELL_SIZE,
                CELL_SIZE,
                color,
            )
        for col, row in piece:
            self._draw_beveled_block(
                BOARD_X + col * CELL_SIZE,
                BOARD_Y + row * CELL_SIZE,
                CELL_SIZE,
                piece_color,
            )

    def start_line_clear_effect(self, rows):
        particles = []
        particle_colors = ((0, 235, 255), (167, 105, 255), (255, 255, 255))
        for row in rows:
            for _ in range(18):
                particles.append(
                    {
                        "x": random.uniform(
                            BOARD_X, BOARD_X + BOARD_WIDTH * CELL_SIZE
                        ),
                        "y": BOARD_Y + row * CELL_SIZE + CELL_SIZE / 2,
                        "vx": random.uniform(-190, 190),
                        "vy": random.uniform(-210, -45),
                        "age": 0,
                        "life": random.uniform(0.28, 0.58),
                        "size": random.randint(2, 5),
                        "color": random.choice(particle_colors),
                    }
                )
        self.line_clear_effects.append(
            {"rows": rows, "elapsed": 0, "particles": particles}
        )
        if self.line_clear_sound is not None:
            self.line_clear_sound.play()

    def _draw_line_clear_effects(self, delta_time):
        self.line_clear_effect_layer.fill((0, 0, 0, 0))
        active_effects = []
        for effect in self.line_clear_effects:
            effect["elapsed"] += delta_time
            elapsed = effect["elapsed"]
            if elapsed < 0.2:
                sweep_width = int(
                    BOARD_WIDTH * CELL_SIZE * min(elapsed / 0.2, 1)
                )
                alpha = int(210 * (1 - elapsed / 0.2))
                for row in effect["rows"]:
                    y = BOARD_Y + row * CELL_SIZE
                    pygame.draw.rect(
                        self.line_clear_effect_layer,
                        (0, 220, 255, alpha // 3),
                        (BOARD_X, y, sweep_width, CELL_SIZE),
                    )
                    pygame.draw.line(
                        self.line_clear_effect_layer,
                        (190, 250, 255, alpha),
                        (BOARD_X + sweep_width, y + 2),
                        (BOARD_X + sweep_width, y + CELL_SIZE - 2),
                        3,
                    )

            remaining_particles = []
            for particle in effect["particles"]:
                particle["age"] += delta_time
                if particle["age"] >= particle["life"]:
                    continue
                particle["x"] += particle["vx"] * delta_time
                particle["y"] += particle["vy"] * delta_time
                particle["vy"] += 380 * delta_time
                alpha = int(255 * (1 - particle["age"] / particle["life"]))
                pygame.draw.circle(
                    self.line_clear_effect_layer,
                    (*particle["color"], alpha),
                    (int(particle["x"]), int(particle["y"])),
                    particle["size"],
                )
                remaining_particles.append(particle)

            effect["particles"] = remaining_particles
            if elapsed < 0.6 or remaining_particles:
                active_effects.append(effect)

        self.line_clear_effects[:] = active_effects
        self.screen.blit(self.line_clear_effect_layer, (0, 0))

    def _draw_panel(self, score, next_piece, next_piece_color):
        panel_rect = pygame.Rect(520, 50, 240, 600)
        pygame.draw.rect(self.screen, (13, 8, 30), panel_rect.move(6, 7), border_radius=12)
        pygame.draw.rect(self.screen, (35, 24, 67), panel_rect, border_radius=12)
        pygame.draw.rect(
            self.screen, (95, 72, 148), panel_rect, width=2, border_radius=12
        )

        score_label = self.small_font.render("SCORE", True, (186, 169, 225))
        self.screen.blit(score_label, (548, 82))
        score_text = self.score_font.render(f"{score:06}", True, (255, 255, 255))
        self.screen.blit(score_text, (544, 105))
        pygame.draw.line(self.screen, (91, 73, 132), (546, 190), (734, 190), 2)

        next_title = self.menu_font.render("NEXT", True, (0, 220, 220))
        self.screen.blit(next_title, (546, 224))
        preview_rect = pygame.Rect(544, 272, 192, 176)
        pygame.draw.rect(self.screen, (24, 17, 46), preview_rect, border_radius=8)
        pygame.draw.rect(
            self.screen, (78, 59, 119), preview_rect, width=1, border_radius=8
        )

        min_col = min(col for col, _ in next_piece)
        max_col = max(col for col, _ in next_piece)
        min_row = min(row for _, row in next_piece)
        max_row = max(row for _, row in next_piece)
        preview_cell_size = 30
        shape_width = (max_col - min_col + 1) * preview_cell_size
        shape_height = (max_row - min_row + 1) * preview_cell_size
        shape_x = preview_rect.centerx - shape_width // 2
        shape_y = preview_rect.centery - shape_height // 2
        for col, row in next_piece:
            self._draw_beveled_block(
                shape_x + (col - min_col) * preview_cell_size,
                shape_y + (row - min_row) * preview_cell_size,
                preview_cell_size,
                next_piece_color,
            )

    def draw_game(
        self,
        delta_time,
        *,
        score,
        landed_blocks,
        piece,
        piece_color,
        next_piece,
        next_piece_color,
        game_over,
    ):
        self._draw_ambient_background(delta_time)
        self._draw_board(landed_blocks, piece, piece_color)
        self._draw_line_clear_effects(delta_time)
        self._draw_panel(score, next_piece, next_piece_color)

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            message_panel = pygame.Rect(248, 278, 304, 130)
            pygame.draw.rect(self.screen, (28, 19, 53), message_panel, border_radius=12)
            pygame.draw.rect(
                self.screen,
                (126, 92, 198),
                message_panel,
                width=2,
                border_radius=12,
            )
            game_over_text = self.font.render("GAME OVER", True, (255, 255, 255))
            restart_text = self.small_font.render(
                "Press R to restart", True, (190, 180, 214)
            )
            self.screen.blit(
                game_over_text,
                game_over_text.get_rect(center=(WIDTH // 2, 326)),
            )
            self.screen.blit(
                restart_text,
                restart_text.get_rect(center=(WIDTH // 2, 370)),
            )
