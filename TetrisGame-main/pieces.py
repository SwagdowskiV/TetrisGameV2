import random

# Colors that pieces can randomly use
PIECE_COLORS = [
    (0, 150, 255),    # Blue
    (255, 80, 80),    # Red
    (0, 200, 100),    # Green
    (255, 200, 0),    # Yellow
    (180, 80, 255),   # Purple
    (255, 120, 0),    # Orange
    (0, 220, 220)     # Cyan
]

def get_random_color():
    return random.choice(PIECE_COLORS)


def create_new_piece():
    pieces = [
        # I-piece
        [
            (3, 0),
            (4, 0),
            (5, 0),
            (6, 0)
        ],

        # O-piece
        [
            (4, 0),
            (5, 0),
            (4, 1),
            (5, 1)
        ],

        # T-piece
        [
            (4, 0),
            (3, 1),
            (4, 1),
            (5, 1)
        ],

        # S-piece
        [
            (4, 0),
            (5, 0),
            (3, 1),
            (4, 1)
        ],

        # Z-piece
        [
            (3, 0),
            (4, 0),
            (4, 1),
            (5, 1)
        ],

        # J-piece
        [
            (3, 0),
            (3, 1),
            (4, 1),
            (5, 1)
        ],

        # L-piece
        [
            (5, 0),
            (3, 1),
            (4, 1),
            (5, 1)
        ],

        # I-Piece
        [
            (3, 0),
            (3, 1),
            (3, 2),
            (3, 3)  
        ]
    ]

    return random.choice(pieces)


def rotate_piece(piece):
    # Use the first block as the center for now
    center_col, center_row = piece[0]

    rotated_piece = []

    for col, row in piece:
        # Find position relative to center
        relative_col = col - center_col
        relative_row = row - center_row

        # Rotate 90 degrees clockwise
        new_col = -relative_row
        new_row = relative_col

        # Move back to board coordinates
        new_col += center_col
        new_row += center_row

        rotated_piece.append((new_col, new_row))

    return rotated_piece


