import argparse

import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


FEATURE_COLS = ["connection", "mobility", "centrality"]
TARGET_COL = "regression_score"


def load_dataset(path: str) -> pd.DataFrame:
    """Load the feature dataset and drop rows missing required columns."""
    df = pd.read_csv(path)
    needed = FEATURE_COLS + [TARGET_COL]
    missing = [col for col in needed if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in dataset: {missing}")
    return df.dropna(subset=needed)


def train_and_evaluate(df: pd.DataFrame) -> None:
    """Train GradientBoostingRegressor and print MSE/R^2."""
    X = df[FEATURE_COLS]
    y = df[TARGET_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0
    )

    reg = GradientBoostingRegressor(random_state=0)
    reg.fit(X_train, y_train)

    y_pred = reg.predict(X_test)

    print("MSE:", mean_squared_error(y_test, y_pred))
    print("R^2:", r2_score(y_test, y_pred))


def main() -> None:
    parser = argparse.ArgumentParser(description="Train v1 regression model on feature dataset.")
    parser.add_argument(
        "--data",
        default="data/club_positions_features.csv",
        help="Path to CSV with feature columns and regression_score target.",
    )
    args = parser.parse_args()

    df = load_dataset(args.data)
    train_and_evaluate(df)


if __name__ == "__main__":
    main()
