import chess

board = chess.Board()      # start position
print(board)               # ASCII board

fen = board.fen()          # FEN string
board2 = chess.Board(fen)  # reconstruct from FEN

print(board.legal_moves)