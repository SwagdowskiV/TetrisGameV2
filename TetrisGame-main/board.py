
# Board settings
CELL_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

def can_move_down(piece, landed_blocks):
    occupied_positions = [
        (col, row)
        for col, row, color in landed_blocks
    ]

    for col, row in piece:
        next_position = (col, row + 1)

        if next_position in occupied_positions:
            return False

        # Check the bottom of the board
        if row + 1 >= BOARD_HEIGHT:
            return False

    return True

def can_move_horizontal(piece, landed_blocks, direction):
    occupied_positions = [
        (col, row)
        for col, row, color in landed_blocks
    ]

    for col, row in piece:
        new_col = col + direction

        # Check the walls
        if new_col < 0 or new_col >= BOARD_WIDTH:
            return False

        # Check landed blocks
        if (new_col, row) in occupied_positions:
            return False

    return True


def clear_lines(landed_blocks):
    full_rows = []

    # Find completely filled rows
    for row in range(BOARD_HEIGHT):
        blocks_in_row = sum(
            1 for col, block_row, color in landed_blocks
            if block_row == row
        )

        if blocks_in_row == BOARD_WIDTH:
            full_rows.append(row)

    # Remove completed rows
    landed_blocks = [
        (col, row, color)
        for col, row, color in landed_blocks
        if row not in full_rows
    ]

    # Move blocks above cleared rows down
    for cleared_row in sorted(full_rows):
        landed_blocks = [
            (col, row + 1, color) if row < cleared_row
            else (col, row, color)
            for col, row, color in landed_blocks
        ]

    return landed_blocks,len(full_rows)


def is_game_over(piece, landed_blocks):
    occupied_positions = [
        (col, row)
        for col, row, color in landed_blocks
    ]

    for col, row in piece:
        if (col, row) in occupied_positions:
            return True

    return False