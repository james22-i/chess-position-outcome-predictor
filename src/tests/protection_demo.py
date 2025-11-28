"""
Quick demo script to print piece_protection outputs for sample positions.
Run with:
    PYTHONPATH=. python src/tests/protection_demo.py
"""

import chess

from src import protection
from src.tests.sample_positions import test_fens


def main() -> None:
    # Use the Ruy Lopez after 3...a6 (index 1 in sample_positions)
    fen = test_fens[1]
    board = chess.Board(fen)
    print("FEN:", fen)
    print(board)

    squares = ["b5", "c6", "d4", "e8"]  # squares with pieces in this FEN

    for sq in squares:
        piece = board.piece_at(chess.parse_square(sq))
        if piece is None:
            print(f"{sq}: empty square")
            continue
        attackers = protection.square_attackers(board, sq, include_san=True)
        defenders = protection.square_defenders(board, sq, include_san=True)
        print(f"\nFor {sq} ({piece.symbol()}):")
        print("  attackers:", attackers)
        print("  defenders:", defenders)


if __name__ == "__main__":
    main()
