import chess

from src import move_utils, protection


def _normalize_color(color: chess.Color | str) -> chess.Color:
    """Accept chess.WHITE/BLACK or 'white'/'black'."""
    if isinstance(color, str):
        normalized = color.lower()
        if normalized == "white":
            return chess.WHITE
        if normalized == "black":
            return chess.BLACK
        raise ValueError("color must be chess.WHITE/chess.BLACK or 'white'/'black'")
    if color not in (chess.WHITE, chess.BLACK):
        raise ValueError("color must be chess.WHITE or chess.BLACK")
    return color


def position_connection(board: chess.Board, color: chess.Color | str) -> int:
    """
    Measure how "connected" a side is by summing defender counts for its pieces.
    Legal defenders only.
    """
    color = _normalize_color(color)

    total_defenders = 0
    for sq, piece in board.piece_map().items():
        if piece.color != color:
            continue
        defenders = protection.square_defenders(board, chess.square_name(sq), include_san=False)
        total_defenders += len(defenders)

    return total_defenders


#does not yet account for hanging, positive trade and negative trades for potential moves
def position_mobility(board: chess.Board, color: chess.Color | str) -> float:
    """
    Weighted legal moves for a side: bishops/knights/rooks x1.5, queens x2, others x1.

    Args:
        board: python-chess Board instance.
        color: chess.WHITE/chess.BLACK or "white"/"black".
    """
    color = _normalize_color(color)
    weights = {
        chess.KING: 0.5,
        chess.BISHOP: 1.5,
        chess.KNIGHT: 1.5,
        chess.ROOK: 1.5,
        chess.QUEEN: 2.0,
    }

    total_moves = 0.0
    for sq, piece in board.piece_map().items():
        if piece.color != color:
            continue
        move_count = move_utils.piece_moves(board, chess.square_name(sq))
        total_moves += move_count * weights.get(piece.piece_type, 1.0)

    return total_moves


_CENTER_CORE = {chess.D4, chess.E4, chess.D5, chess.E5}
_CENTER_RING = {
    chess.C4,
    chess.F4,
    chess.C5,
    chess.F5,
    chess.D3,
    chess.E3,
    chess.D6,
    chess.E6,
}
_CENTER_CORNERS = {
    chess.C3,
    chess.F3,
    chess.C6,
    chess.F6,
}
_CENTRAL_SQUARES = _CENTER_CORE | _CENTER_RING | _CENTER_CORNERS


def position_centrality(board: chess.Board, color: chess.Color | str) -> int:
    """
    Score central presence: +2 for core (d4, e4, d5, e5); +1 for surrounding ring.
    """
    color = _normalize_color(color)

    count = 0
    for sq in _CENTRAL_SQUARES:
        piece = board.piece_at(sq)
        if piece is None or piece.color != color:
            continue
        if sq in _CENTER_CORE:
            count += 2
        else:
            count += 1
    return count


def position_features(board: chess.Board, color: chess.Color | str) -> dict[str, float | int]:
    """
    Convenience: return core features for the side to move.

    Returns:
        {
            "connection": int,
            "mobility": float,
            "centrality": int,
        }
    """
    color = _normalize_color(color)
    return {
        "connection": position_connection(board, color),
        "mobility": position_mobility(board, color),
        "centrality": position_centrality(board, color),
    }
