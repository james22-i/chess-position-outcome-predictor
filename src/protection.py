"""
<<<<<<< HEAD
Utilities to measure how well pieces are defended/protected on the board.
=======
Utilities to list legal attackers and defenders for a given occupied square.
>>>>>>> 6647404 (filtered dataset and added new variables)
"""

import chess

from src import move_utils


<<<<<<< HEAD
def piece_protection(
    board: chess.Board,
    square: str,
    *,
    legal_only: bool = False,
    include_san: bool = False,
) -> dict:
    """
    Given a board and a square (assumed occupied), return pieces that could recapture
    on that square if the piece were taken (square treated as empty for analysis).

    Args:
        board: python-chess Board instance.
        square: Algebraic square name of the piece to evaluate (e.g., "e4").
        legal_only: If True, only include legal defenders after the square is emptied
                    (filters pinned/illegal even in the hypothetical capture state).
        include_san: If True, include SAN strings for legal defender moves.

    Returns:
        {
            "square": str,
            "piece": symbol,
            "color": "white"/"black",
            "defenders": [...],
            "defender_count": int,
        }
    """
=======
def _validate_piece_on_square(board: chess.Board, square: str) -> tuple[int, chess.Piece]:
    """Parse square and ensure a piece is present."""
>>>>>>> 6647404 (filtered dataset and added new variables)
    try:
        sq = chess.parse_square(square)
    except ValueError as exc:
        raise ValueError(f"Invalid square '{square}'") from exc

    piece = board.piece_at(sq)
    if piece is None:
        raise ValueError(f"No piece on square '{square}'")
<<<<<<< HEAD

    # Treat the target square as empty (piece captured) to find potential recaptures.
=======
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

>>>>>>> 6647404 (filtered dataset and added new variables)
    temp_board = board.copy(stack=False)
    temp_board.remove_piece_at(sq)

    analysis = move_utils.square_analysis(
        temp_board,
        square,
<<<<<<< HEAD
        legal_only=legal_only,
        include_san=include_san,
        include_legal_flag=True,
    )

    defenders = analysis["white"] if piece.color == chess.WHITE else analysis["black"]

    return {
        "square": square,
        "piece": piece.symbol(),
        "color": "white" if piece.color == chess.WHITE else "black",
        "defenders": defenders,
        "defender_count": len(defenders),
    }
=======
        legal_only=True,
        include_san=include_san,
        include_legal_flag=False,
    )

    return analysis["white"] if piece.color == chess.WHITE else analysis["black"]
>>>>>>> 6647404 (filtered dataset and added new variables)
