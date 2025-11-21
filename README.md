# Chess Win Probability Model

Goal: Given a chess position, estimate the probability that either side eventually wins the game. A side goal is to establish a simple determinable variable which is a good indicator of which side is winning.

This project will:
- Parse a collection of chess games into positions and outcomes.
- Engineer interpretable features from each position (e.g., material, king safety, game phase).
- Train and evaluate models (e.g., logistic regression, tree-based models) to predict win probabilities.
- Analyse calibration, feature importance, and model limitations.

## Project structure

- `src/` – data processing, feature engineering, and modelling code.
- `data/` – raw/processed data (not tracked in Git if large).
- `notebooks/` – exploratory analysis and visualisations.
- `requirements.txt` – Python dependencies.

## Status

Early setup – repository structure and environment only.