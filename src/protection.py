"""
Utilities to measure how well pieces are defended/protected on the board.
"""

import chess

from src import move_utils


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
    try:
        sq = chess.parse_square(square)
    except ValueError as exc:
        raise ValueError(f"Invalid square '{square}'") from exc

    piece = board.piece_at(sq)
    if piece is None:
        raise ValueError(f"No piece on square '{square}'")

    # Treat the target square as empty (piece captured) to find potential recaptures.
    temp_board = board.copy(stack=False)
    temp_board.remove_piece_at(sq)

    analysis = move_utils.square_analysis(
        temp_board,
        square,
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
