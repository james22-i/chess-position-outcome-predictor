import chess


def moves_for_piece(
    board: chess.Board,
    square: str,
    *,
    legal_only: bool = True,
    san: bool = False,
) -> list[str]:
    """
    Return moves for the piece on the given square.

    Args:
        board: python-chess Board instance.
        square: Algebraic square name like "e4".
        legal_only: If False, use pseudo-legal moves (ignore check).
        san: If True, return SAN strings; otherwise return UCI strings.
    """
    try:
        sq = chess.parse_square(square)
    except ValueError as exc:
        raise ValueError(f"Invalid square '{square}'") from exc

    piece = board.piece_at(sq)
    if piece is None:
        raise ValueError(f"No piece on square '{square}'")

    move_iter = board.legal_moves if legal_only else board.generate_pseudo_legal_moves()
    moves = [m for m in move_iter if m.from_square == sq]

    if san:
        if not legal_only:
            raise ValueError("SAN output requires legal_only=True")
        return [board.san(m) for m in moves]

    return [m.uci() for m in moves]


def piece_moves(
    board: chess.Board,
    square: str,
    piece_symbol: str | None = None,
) -> int:
    """
    Count the number of legal moves for the piece on the given square.

    Args:
        board: python-chess Board instance.
        square: Algebraic square name like "e4".
        piece_symbol: Optional expected piece symbol (e.g., "N", "p") to validate.

    Returns:
        Integer count of legal moves for the piece on the square.
    """
    moves = moves_for_piece(board, square, legal_only=True, san=False)

    if piece_symbol is not None:
        sq = chess.parse_square(square)
        piece = board.piece_at(sq)
        if piece is None:
            raise ValueError(f"No piece on square '{square}'")
        if piece.symbol() != piece_symbol:
            raise ValueError(
                f"Piece mismatch at '{square}': found '{piece.symbol()}', expected '{piece_symbol}'"
            )

    return len(moves)


def square_analysis(
    board: chess.Board,
    square: str,
    *,
    legal_only: bool = False,
    include_san: bool = False,
    include_legal_flag: bool = True,
) -> dict[str, list[dict]]:
    """
    Return pieces that are attacking/protecting a target square in the current position.

    Args:
        board: python-chess Board instance.
        square: Target square (e.g., "e4").
        legal_only: If True, only include pieces whose move to the square is legal
                    (filters out pinned pieces or illegal due to check/occupancy).
        include_san: If True, include SAN strings for the move to the square (legal moves only).
        include_legal_flag: If True, annotate each entry with an "is_legal" boolean.

    Returns:
        Dict with keys "white" and "black", each a list of dicts:
        {"from", "piece", "color", "uci", (optional) "san"}.
    """
    try:
        target_sq = chess.parse_square(square)
    except ValueError as exc:
        raise ValueError(f"Invalid square '{square}'") from exc

    legal_moves_set = set(board.legal_moves) if (legal_only or include_san or include_legal_flag) else None

    attackers = {
        "white": board.attackers(chess.WHITE, target_sq),
        "black": board.attackers(chess.BLACK, target_sq),
    }

    def _entries(side: chess.Color) -> list[dict]:
        entries: list[dict] = []
        for from_sq in attackers["white" if side == chess.WHITE else "black"]:
            piece = board.piece_at(from_sq)
            if piece is None:
                continue
            move = chess.Move(from_sq, target_sq)
            is_legal = move in legal_moves_set if legal_moves_set is not None else False
            if legal_only and not is_legal:
                continue
            entry = {
                "from": chess.square_name(from_sq),
                "piece": piece.symbol(),
                "color": "white" if piece.color == chess.WHITE else "black",
                "uci": move.uci(),
            }
            if include_legal_flag:
                entry["is_legal"] = is_legal
            if include_san and is_legal:
                entry["san"] = board.san(move)
            entries.append(entry)
        return entries

    return {
        "white": _entries(chess.WHITE),
        "black": _entries(chess.BLACK),
    }


def hanging(board: chess.Board, square: str) -> bool:
    """
    Indicator: True if the piece on `square` is attacked and undefended.

    Args:
        board: python-chess Board instance.
        square: Algebraic square name like "e4".
    """
    try:
        target_sq = chess.parse_square(square)
    except ValueError as exc:
        raise ValueError(f"Invalid square '{square}'") from exc

    piece = board.piece_at(target_sq)
    if piece is None:
        raise ValueError(f"No piece on square '{square}'")

    color = piece.color
    enemy = not color

    # Pseudo-legal attackers/defenders (includes pinned pieces).
    attackers = board.attackers(enemy, target_sq)
    defenders = board.attackers(color, target_sq)

    return len(attackers) > 0 and len(defenders) == 0
