"""
Utilities to list legal attackers and defenders for a given occupied square.
"""

import chess

from src import move_utils


def _validate_piece_on_square(board: chess.Board, square: str) -> tuple[int, chess.Piece]:
    """Parse square and ensure a piece is present."""
    try:
        sq = chess.parse_square(square)
    except ValueError as exc:
        raise ValueError(f"Invalid square '{square}'") from exc

    piece = board.piece_at(sq)
    if piece is None:
        raise ValueError(f"No piece on square '{square}'")

    return sq, piece


def square_attackers(
    board: chess.Board,
    square: str,
    *,
    include_san: bool = False,
) -> list[dict]:
    """
    Return opposing pieces that can legally capture the piece on the target square.

    Args:
        board: python-chess Board instance.
        square: Algebraic square name of the piece to evaluate (e.g., "e4").
        include_san: If True, include SAN strings for the capture move.
    """
    _, piece = _validate_piece_on_square(board, square)

    analysis = move_utils.square_analysis(
        board,
        square,
        legal_only=True,
        include_san=include_san,
        include_legal_flag=False,
    )

    return analysis["black"] if piece.color == chess.WHITE else analysis["white"]


def square_defenders(
    board: chess.Board,
    square: str,
    *,
    include_san: bool = False,
) -> list[dict]:
    """
    Return same-color pieces that could legally move to the square to recapture if it were taken.

    The target square is treated as empty to allow the defenders to move onto it.

    Args:
        board: python-chess Board instance.
        square: Algebraic square name of the piece to evaluate (e.g., "e4").
        include_san: If True, include SAN strings for the recapture move.
    """
    sq, piece = _validate_piece_on_square(board, square)

    temp_board = board.copy(stack=False)
    temp_board.remove_piece_at(sq)

    analysis = move_utils.square_analysis(
        temp_board,
        square,
        legal_only=True,
        include_san=include_san,
        include_legal_flag=False,
    )

    return analysis["white"] if piece.color == chess.WHITE else analysis["black"]
