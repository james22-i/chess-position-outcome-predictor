import chess

from src import move_utils, protection


def position_connection(board: chess.Board, color: chess.Color | str) -> int:
    """
    Measure how "connected" a side is by summing defender counts for all its pieces.

    Args:
        board: python-chess Board instance.
        color: chess.WHITE/chess.BLACK or "white"/"black".

    Returns:
        Integer sum of how many defenders each piece has (legal defenders only).
    """
    if isinstance(color, str):
        normalized = color.lower()
        if normalized == "white":
            color = chess.WHITE
        elif normalized == "black":
            color = chess.BLACK
        else:
            raise ValueError("color must be chess.WHITE/chess.BLACK or 'white'/'black'")
    elif color not in (chess.WHITE, chess.BLACK):
        raise ValueError("color must be chess.WHITE or chess.BLACK")

    total_defenders = 0
    for sq, piece in board.piece_map().items():
        if piece.color != color:
            continue
        defenders = protection.square_defenders(board, chess.square_name(sq), include_san=False)
        total_defenders += len(defenders)

    return total_defenders


#does not yet account for hanging, positive trade and negative trades for potential moves
def position_mobility(board: chess.Board, color: chess.Color | str) -> int:
    """
    Total number of legal moves available to all pieces of a side.

    Args:
        board: python-chess Board instance.
        color: chess.WHITE/chess.BLACK or "white"/"black".
    """
    if isinstance(color, str):
        normalized = color.lower()
        if normalized == "white":
            color = chess.WHITE
        elif normalized == "black":
            color = chess.BLACK
        else:
            raise ValueError("color must be chess.WHITE/chess.BLACK or 'white'/'black'")
    elif color not in (chess.WHITE, chess.BLACK):
        raise ValueError("color must be chess.WHITE or chess.BLACK")

    total_moves = 0
    for sq, piece in board.piece_map().items():
        if piece.color != color:
            continue
        # piece_moves will raise if the square is empty, so no extra guard needed.
        total_moves += move_utils.piece_moves(board, chess.square_name(sq))

    return total_moves


def position_centrality(board: chess.Board) -> dict[str, int]:
    """
    Count how many pieces of each side occupy the central 4x4 squares.

    Returns:
        {"white": count, "black": count}
    """
    central_squares = [
        chess.C4,
        chess.D4,
        chess.E4,
        chess.F4,
        chess.C5,
        chess.D5,
        chess.E5,
        chess.F5,
        chess.C3,
        chess.D3,
        chess.E3,
        chess.F3,
        chess.C6,
        chess.D6,
        chess.E6,
        chess.F6,
    ]

    counts = {"white": 0, "black": 0}
    for sq in central_squares:
        piece = board.piece_at(sq)
        if piece is None:
            continue
        if piece.color == chess.WHITE:
            counts["white"] += 1
        else:
            counts["black"] += 1

    return counts
