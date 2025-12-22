import argparse
import pandas as pd
from model_utils import engineer_features, train_and_save_model


def main():
    parser = argparse.ArgumentParser(description="Train predictive maintenance model")
    parser.add_argument("--input", "-i", required=True, help="Path to training CSV")
    parser.add_argument("--target", "-t", default=None, help="Target column name (default: Failure or Mileage (km))")
    parser.add_argument("--output", "-o", default="saved_models/latest_model.joblib", help="Output model path")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    df = engineer_features(df)

    if args.target:
        target_col = args.target
    elif "Failure" in df.columns:
        target_col = "Failure"
    else:
        target_col = "Mileage (km)"

    X = df.drop(columns=[target_col])
    y = df[target_col]

    path = train_and_save_model(X, y, args.output)
    print(f"Model saved to: {path}")


if __name__ == "__main__":
    main()
