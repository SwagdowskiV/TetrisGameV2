import pygame

from board import (
    BOARD_HEIGHT,
    BOARD_WIDTH,
    can_move_down,
    can_move_horizontal,
    clear_lines,
    is_game_over,
)
from graphics import Graphics
from pieces import create_new_piece, get_random_color, rotate_piece


class Game:
    FALL_SPEED = 500

    def __init__(self):
        pygame.init()
        self.graphics = Graphics()
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen_state = "menu"
        self.score = 0
        self.game_over = False
        self.landed_blocks = []
        self.piece = create_new_piece()
        self.piece_color = get_random_color()
        self.next_piece = create_new_piece()
        self.next_piece_color = get_random_color()
        self.last_fall_time = pygame.time.get_ticks()

    def start_game(self):
        self.piece = create_new_piece()
        self.piece_color = get_random_color()
        self.next_piece = create_new_piece()
        self.next_piece_color = get_random_color()
        self.landed_blocks = []
        self.score = 0
        self.game_over = False
        self.last_fall_time = pygame.time.get_ticks()
        self.graphics.reset_effects()
        self.screen_state = "playing"

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            return

        if self.screen_state == "menu":
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.graphics.play_button.collidepoint(event.pos)
            ):
                self.start_game()
            elif event.type == pygame.KEYDOWN and event.key in (
                pygame.K_RETURN,
                pygame.K_SPACE,
            ):
                self.start_game()
            return

        if event.type != pygame.KEYDOWN:
            return

        if self.game_over:
            if event.key == pygame.K_r:
                self.start_game()
            return

        if event.key in (pygame.K_LEFT, pygame.K_a):
            if can_move_horizontal(self.piece, self.landed_blocks, -1):
                self.piece = [(col - 1, row) for col, row in self.piece]
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            if can_move_horizontal(self.piece, self.landed_blocks, 1):
                self.piece = [(col + 1, row) for col, row in self.piece]
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            if can_move_down(self.piece, self.landed_blocks):
                self.piece = [(col, row + 1) for col, row in self.piece]
        elif event.key in (pygame.K_UP, pygame.K_w):
            self.piece = rotate_piece(self.piece)

    def _lock_piece(self):
        for col, row in self.piece:
            self.landed_blocks.append((col, row, self.piece_color))

        full_rows = [
            row
            for row in range(BOARD_HEIGHT)
            if sum(
                1
                for _, block_row, _ in self.landed_blocks
                if block_row == row
            )
            == BOARD_WIDTH
        ]
        self.landed_blocks, lines_cleared = clear_lines(self.landed_blocks)
        if lines_cleared:
            self.graphics.start_line_clear_effect(full_rows)
        self.score += lines_cleared * 100

        self.piece = self.next_piece
        self.piece_color = self.next_piece_color
        self.next_piece = create_new_piece()
        self.next_piece_color = get_random_color()
        if is_game_over(self.piece, self.landed_blocks):
            self.game_over = True

    def update(self, delta_time):
        if self.screen_state != "playing":
            return

        current_time = pygame.time.get_ticks()
        if (
            not self.game_over
            and current_time - self.last_fall_time >= self.FALL_SPEED
        ):
            if can_move_down(self.piece, self.landed_blocks):
                self.piece = [(col, row + 1) for col, row in self.piece]
            else:
                self._lock_piece()
            self.last_fall_time = current_time

    def draw(self, delta_time):
        if self.screen_state == "menu":
            self.graphics.draw_menu(delta_time)
        else:
            self.graphics.draw_game(
                delta_time,
                score=self.score,
                landed_blocks=self.landed_blocks,
                piece=self.piece,
                piece_color=self.piece_color,
                next_piece=self.next_piece,
                next_piece_color=self.next_piece_color,
                game_over=self.game_over,
            )

    def run(self):
        try:
            while self.running:
                delta_time = self.clock.tick(100) / 1000
                for event in pygame.event.get():
                    self.handle_event(event)
                self.update(delta_time)
                self.draw(delta_time)
                pygame.display.flip()
        finally:
            pygame.quit()


if __name__ == "__main__":
    Game().run()
