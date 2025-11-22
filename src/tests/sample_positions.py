test_fens = [
    # --- Opening / early game ---
    # 1. Starting position
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",

    # 2. Ruy Lopez after 3...a6
    "r1bqkbnr/1pp1pppp/p1np4/1B2P3/3P4/5N2/PPP2PPP/RNBQK2R b KQkq - 1 5",

    # 3. Sicilian Defence, basic Open Sicilian structure
    "rnbqk2r/pp2ppbp/3p1np1/2pP4/2P5/2N2NP1/PP2PPBP/R1BQK2R w KQkq - 0 7",

    # 4. Queen’s Gambit Declined structure
    "rnbq1rk1/ppp1bppp/3p1n2/2pPp3/2P1P3/2N2N2/PP2BPPP/R1BQ1RK1 w - - 4 9",

    # 5. King’s Indian Defence style structure
    "rnbq1rk1/pp2ppbp/3p1np1/2pP4/2P1P3/2N2N2/PP2BPPP/R1BQ1RK1 w - - 5 8",

    # --- Middlegame positions ---
    # 6. Sharp attacking middlegame (opposite-side castling)
    "r1bq1rk1/pp1n1ppp/2p1pn2/2Pp4/3P1B2/2N1PN2/PP3PPP/R2Q1RK1 b - - 2 11",

    # 7. Isolated queen’s pawn middlegame
    "r1bq1rk1/pp3ppp/2nbpn2/2pp4/3P4/2PBPN2/PP1N1PPP/R1BQ1RK1 w - - 2 9",

    # 8. Semi-open file, central tension
    "r2q1rk1/pp1bppbp/3p1np1/2pP4/2P1P3/2N1BN2/PPQ1BPPP/R3K2R w KQ - 4 10",

    # 9. Typical minority attack structure
    "r1bq1rk1/1p1n1ppp/p2bpn2/2pp4/3P4/2PBPN2/PP1N1PPP/R1BQ1RK1 w - - 4 10",

    # 10. Tactical middlegame with open centre
    "r1bq1rk1/pp2bppp/2n1pn2/2pp4/3P4/2PBPN2/PPQN1PPP/R1B2RK1 w - - 6 11",

    # --- Endgames ---
    # 11. Simple king and pawn vs king
    "8/8/8/4k3/4P3/8/8/4K3 w - - 0 40",

    # 12. Rook and pawn vs rook
    "8/8/8/4k3/3rP3/8/4R3/4K3 w - - 0 60",

    # 13. Bishop and pawn vs bishop (same colour)
    "8/8/4k3/4p3/4B3/8/4b3/4K3 w - - 0 50",

    # 14. Queen vs rook endgame
    "8/8/8/4k3/4q3/8/5R2/4K3 w - - 0 70",

    # 15. Knight and pawn vs knight
    "8/8/8/4k3/4p3/4N3/4n3/4K3 w - - 0 50",
]
