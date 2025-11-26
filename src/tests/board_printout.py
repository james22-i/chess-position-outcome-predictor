import chess
from src import move_utils
from src import protection

# Start position
board = chess.Board()
print(board)

# Example FEN from an article – needs to be a quoted string
fen = "r1b1k2N/ppp1q1pp/2n2n2/3p4/2B1P3/8/PPPP1bPP/RNBQ1K1R w q d6 0 1"
board2 = chess.Board(fen)
print(f"FEN: {fen}")
print(board2)  # ASCII board reconstructed from FEN

# Moves available to the knight on h8 in this position
knight_moves_san = move_utils.moves_for_piece(board2, "h8", san=True)
print("Legal moves for white knight on h8:", knight_moves_san)

# Pieces attacking/protecting f1 in the current position
square_analysis_f1 = move_utils.square_analysis(board2, "f1", include_san=True)
print("Attackers/protectors of f1 ->", square_analysis_f1)

# Same, but filter to legal moves only (drops pinned/illegal moves)
square_analysis_f1_legal = move_utils.square_analysis(board2, "f1", include_san=True, legal_only=True)
print("Attackers/protectors of f1 (legal only) ->", square_analysis_f1_legal)

<<<<<<< HEAD
# Protection info for a few squares (defenders only)
for sq in ["f1", "h8", "e8"]:
    try:
        info = protection.piece_protection(board2, sq, legal_only=False, include_san=False)
        print(f"Protection for {sq} ({info['piece']}): defenders={info['defender_count']}, list={info['defenders']}")
=======
# Attackers/defenders for a few squares (legal moves only)
for sq in ["f1", "h8", "e8"]:
    try:
        attackers = protection.square_attackers(board2, sq, include_san=False)
        defenders = protection.square_defenders(board2, sq, include_san=False)
        piece = board2.piece_at(chess.parse_square(sq)).symbol()
        print(f"For {sq} ({piece}): attackers={len(attackers)}, defenders={len(defenders)}")
        print("   attacker list:", attackers)
        print("   defender list:", defenders)
>>>>>>> 6647404 (filtered dataset and added new variables)
    except ValueError as exc:
        print(f"{sq}: {exc}")
