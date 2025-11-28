import chess
import pandas as pd

from src import features


def _result_to_winner(result: str | None) -> str:
    """Map PGN-style result strings to 'white'/'black'/'draw'/'unknown'."""
    if not result:
        return "unknown"
    res = result.strip()
    if res == "1-0":
        return "white"
    if res == "0-1":
        return "black"
    if res in ("1/2-1/2", "1/2", "1-1"):
        return "draw"
    return "unknown"


def features_from_fen(fen: str) -> dict[str, int | str]:
    """
    Compute feature metrics for the side to move in a given FEN string.

    Returns: side_to_move, connection, mobility, centrality.
    """
    board = chess.Board(fen)
    side = "white" if board.turn == chess.WHITE else "black"

    vals = features.position_features(board, board.turn)
    return {
        "side_to_move": side,
        "connection": vals["connection"],
        "mobility": vals["mobility"],
        "centrality": vals["centrality"],
    }


def evaluate_positions_with_side(
    csv_path: str,
    *,
    side_col: str = "side_to_move",
    fen_col: str = "fen",
    result_col: str = "result",
    max_rows: int | None = None,
) -> pd.DataFrame:
    """
    Load a CSV with side_to_move, FEN, and result columns and compute features for each row.

    Returns a DataFrame with: index, side_to_move, connection, mobility, centrality, result, winning_side.
    """
    df = pd.read_csv(csv_path)
    if max_rows is not None:
        df = df.head(max_rows)

    records: list[dict] = []
    for idx, row in df.iterrows():
        fen = row.get(fen_col)
        side_raw = row.get(side_col)
        result = row.get(result_col)

        if not isinstance(fen, str) or not fen.strip() or not isinstance(side_raw, str):
            continue

        side_normalized = side_raw.lower()
        if side_normalized not in ("white", "black"):
            continue
        color = chess.WHITE if side_normalized == "white" else chess.BLACK

        board = chess.Board(fen)
        vals = features.position_features(board, color)

        winning_side = _result_to_winner(result)
        if winning_side == "draw":
            regression_score = 0.5
        elif winning_side == side_normalized:
            regression_score = 1.0
        else:
            regression_score = 0.0

        records.append(
            {
                "index": idx,
                "side_to_move": side_normalized,
                "connection": vals["connection"],
                "mobility": vals["mobility"],
                "centrality": vals["centrality"],
                "result": result,
                "winning_side": winning_side,
                "regression_score": regression_score,
            }
        )

    return pd.DataFrame(records)
