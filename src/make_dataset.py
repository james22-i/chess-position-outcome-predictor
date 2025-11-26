"""
Utilities to convert chess game data into a flat dataset of positions (from PGN or CSV).

Usage:
    PYTHONPATH=. python src/make_dataset.py --pgn data/games.pgn --output data/positions.csv
    PYTHONPATH=. python src/make_dataset.py --csv data/games.csv --output data/positions.parquet
    PYTHONPATH=. python src/make_dataset.py --club-csv data/club_games_data.csv --output data/club_positions.csv
"""

import argparse
import io
import pathlib
from typing import Iterable

import chess
import chess.pgn
import pandas as pd


def _positions_from_game(game: chess.pgn.Game, game_index: int) -> Iterable[dict]:
    """Yield position records for each ply in a single game."""
    board = game.board()
    result = game.headers.get("Result", "*")

    for ply, move in enumerate(game.mainline_moves(), start=1):
        san = board.san(move)
        uci = move.uci()
        board.push(move)
        yield {
            "game_index": game_index,
            "ply": ply,
            "move_number": (ply + 1) // 2,
            "side_to_move": "white" if board.turn == chess.WHITE else "black",
            "fen": board.fen(),
            "uci": uci,
            "san": san,
            "result": result,
        }


def load_pgn_positions(pgn_path: str | pathlib.Path, max_games: int | None = None) -> pd.DataFrame:
    """
    Load positions from a PGN file into a DataFrame.

    Args:
        pgn_path: Path to a PGN file.
        max_games: Optional limit on number of games to parse.
    """
    records: list[dict] = []
    pgn_path = pathlib.Path(pgn_path)

    with pgn_path.open("r", encoding="utf-8") as handle:
        game_idx = 0
        while True:
            if max_games is not None and game_idx >= max_games:
                break
            game = chess.pgn.read_game(handle)
            if game is None:
                break
            game_idx += 1
            records.extend(_positions_from_game(game, game_idx))

    return pd.DataFrame(records)


def _winner_to_result(winner: str) -> str:
    winner = (winner or "").lower()
    if winner == "white":
        return "1-0"
    if winner == "black":
        return "0-1"
    if winner == "draw":
        return "1/2-1/2"
    return "*"


def _color_results_to_result(white_result: str | None, black_result: str | None) -> str | None:
    wr = (white_result or "").lower()
    br = (black_result or "").lower()
    if wr == "win" or br == "checkmated" or br == "timeout":
        return "1-0"
    if br == "win" or wr == "checkmated" or wr == "timeout":
        return "0-1"
    if wr == "draw" or br == "draw":
        return "1/2-1/2"
    return None


def load_csv_positions(csv_path: str | pathlib.Path, max_games: int | None = None) -> pd.DataFrame:
    """
    Load positions from a CSV file with a 'moves' column of SAN strings.

    Expected columns (minimum): id (optional), moves (space-separated SAN), winner (optional).
    """
    csv_path = pathlib.Path(csv_path)
    df_games = pd.read_csv(csv_path)

    records: list[dict] = []
    for idx, row in df_games.iterrows():
        if max_games is not None and idx >= max_games:
            break

        moves_raw = row.get("moves", "")
        if pd.isna(moves_raw) or not isinstance(moves_raw, str) or not moves_raw.strip():
            continue

        board = chess.Board()
        result = _winner_to_result(row.get("winner", "*"))
        game_id = row.get("id", idx + 1)
        game_index = idx + 1

        for ply, san in enumerate(moves_raw.split(), start=1):
            move = board.parse_san(san)
            uci = move.uci()
            board.push(move)
            records.append(
                {
                    "game_id": game_id,
                    "game_index": game_index,
                    "ply": ply,
                    "move_number": (ply + 1) // 2,
                    "side_to_move": "white" if board.turn == chess.WHITE else "black",
                    "fen": board.fen(),
                    "uci": uci,
                    "san": san,
                    "result": result,
                }
            )

    return pd.DataFrame(records)


def _time_control_seconds(tc: str) -> int | None:
    """Convert chess.com-style time control strings to approximate total initial seconds per side."""
    if pd.isna(tc):
        return None
    if not isinstance(tc, str):
        tc = str(tc)
    if not tc:
        return None
    if "/" in tc:
        # Daily format like "1/259200" (increment per move in seconds)
        parts = tc.split("/")
        try:
            return int(parts[-1])
        except ValueError:
            return None
    if "+" in tc:
        base, inc = tc.split("+", 1)
        try:
            base_sec = int(base)
        except ValueError:
            return None
        return base_sec  # ignore increment for filtering
    try:
        return int(tc)
    except ValueError:
        return None


def load_club_csv_positions(
    csv_path: str | pathlib.Path,
    *,
    max_games: int | None = None,
    min_rating: int = 1700,
    min_time_control_seconds: int = 600,
    min_move_number: int = 11,
) -> pd.DataFrame:
    """
    Load and filter club game data (chess.com CSV with PGN column).

    Filters:
      - Both ratings >= min_rating.
      - Time control >= min_time_control_seconds (per side).
      - Only positions with move_number >= min_move_number (i.e., after move 10 by default).
    """
    csv_path = pathlib.Path(csv_path)
    df_games = pd.read_csv(csv_path)

    records: list[dict] = []

    for idx, row in df_games.iterrows():
        if max_games is not None and idx >= max_games:
            break

        white_rating = row.get("white_rating")
        black_rating = row.get("black_rating")
        tc_seconds = _time_control_seconds(row.get("time_control"))

        if pd.isna(white_rating) or pd.isna(black_rating):
            continue
        if int(white_rating) < min_rating or int(black_rating) < min_rating:
            continue
        if tc_seconds is None or tc_seconds < min_time_control_seconds:
            continue

        pgn_text = row.get("pgn")
        if not isinstance(pgn_text, str) or not pgn_text.strip():
            continue

        game = chess.pgn.read_game(io.StringIO(pgn_text))
        if game is None:
            continue

        result = game.headers.get("Result")
        if not result or result == "*":
            color_result = _color_results_to_result(row.get("white_result"), row.get("black_result"))
            if color_result:
                result = color_result
            else:
                result = _winner_to_result(row.get("winner")) if "winner" in row else "*"

        board = game.board()
        game_id = row.get("id", idx + 1)
        game_index = idx + 1

        for ply, move in enumerate(game.mainline_moves(), start=1):
            san = board.san(move)
            board.push(move)
            move_number = (ply + 1) // 2
            if move_number < min_move_number:
                continue
            records.append(
                {
                    "game_id": game_id,
                    "game_index": game_index,
                    "ply": ply,
                    "move_number": move_number,
                    "side_to_move": "white" if board.turn == chess.WHITE else "black",
                    "fen": board.fen(),
                    "uci": move.uci(),
                    "san": san,
                    "result": result or "*",
                    "white_rating": int(white_rating),
                    "black_rating": int(black_rating),
                    "time_control": row.get("time_control"),
                }
            )

    return pd.DataFrame(records)


def _write_output(df: pd.DataFrame, output_path: str | pathlib.Path, fmt: str) -> None:
    output_path = pathlib.Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if fmt == "csv":
        df.to_csv(output_path, index=False)
    elif fmt == "parquet":
        df.to_parquet(output_path, index=False)
    else:
        raise ValueError(f"Unsupported format '{fmt}'")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract positions from PGN or CSV into a flat dataset.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--pgn", help="Path to PGN file.")
    source.add_argument("--csv", help="Path to CSV file with SAN moves.")
    source.add_argument(
        "--club-csv",
        help="Path to Chess.com club CSV (expects ratings, time_control, and PGN columns).",
    )
    parser.add_argument("--output", required=True, help="Output file path (csv or parquet).")
    parser.add_argument(
        "--format",
        choices=["csv", "parquet"],
        help="Output format (inferred from extension if omitted).",
    )
    parser.add_argument("--max-games", type=int, default=None, help="Optional limit on games to parse.")

    args = parser.parse_args()

    out_fmt = args.format
    if out_fmt is None:
        suffix = pathlib.Path(args.output).suffix.lower()
        if suffix == ".parquet":
            out_fmt = "parquet"
        else:
            out_fmt = "csv"

    if args.pgn:
        df = load_pgn_positions(args.pgn, max_games=args.max_games)
    elif args.csv:
        df = load_csv_positions(args.csv, max_games=args.max_games)
    else:
        df = load_club_csv_positions(args.club_csv, max_games=args.max_games)

    if df.empty:
        raise SystemExit("No positions extracted (empty PGN or zero games parsed).")

    _write_output(df, args.output, out_fmt)
    print(f"Wrote {len(df)} positions to {args.output} ({out_fmt}).")


if __name__ == "__main__":
    main()
