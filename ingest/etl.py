import os
from typing import Tuple

import numpy as np
import pandas as pd


def validate_schema(df: pd.DataFrame) -> Tuple[bool, list]:
    """Basic validation: ensure `vehicle_id` and `timestamp` exist."""
    required = ["vehicle_id", "timestamp"]
    missing = [c for c in required if c not in df.columns]
    return (len(missing) == 0), missing


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean telemetry DataFrame:
    - parse timestamps
    - drop rows missing `vehicle_id` or `timestamp`
    - drop exact duplicates
    - coerce negative numeric values to NaN and fill with median
    """
    df = df.copy()
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # remove rows without id or timestamp
    drop_cols = [c for c in ("vehicle_id", "timestamp") if c in df.columns]
    if drop_cols:
        df = df.dropna(subset=drop_cols)

    df = df.drop_duplicates()

    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    for c in num_cols:
        # negative values don't make sense for many telemetry features
        df.loc[df[c] < 0, c] = np.nan
        if df[c].notna().any():
            med = df[c].median()
            df[c] = df[c].fillna(med)
        else:
            df[c] = df[c].fillna(0)

    return df


def normalize_features(df: pd.DataFrame, method: str = "zscore") -> pd.DataFrame:
    """Add normalized columns for numeric features. Two methods supported: `zscore` and `minmax`.
    Adds new columns with suffixes `_z` or `_scaled`.
    """
    df = df.copy()
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    for c in num_cols:
        if method == "zscore":
            mean = df[c].mean()
            std = df[c].std()
            denom = std if std != 0 and not np.isnan(std) else 1.0
            df[c + "_z"] = (df[c] - mean) / denom
        else:
            minv = df[c].min()
            maxv = df[c].max()
            denom = (maxv - minv) if maxv != minv else 1.0
            df[c + "_scaled"] = (df[c] - minv) / denom
    return df


def process_file(input_path: str, output_path: str = None, normalize_method: str = "zscore"):
    """Read CSV, validate, clean, normalize, and optionally write out cleaned CSV.

    Returns the cleaned DataFrame or path to written file.
    """
    df = pd.read_csv(input_path)
    ok, missing = validate_schema(df)
    if not ok:
        raise ValueError(f"Missing required columns: {missing}")

    df = clean_data(df)
    df = normalize_features(df, method=normalize_method)

    if output_path:
        folder = os.path.dirname(output_path) or "."
        os.makedirs(folder, exist_ok=True)
        df.to_csv(output_path, index=False)
        return output_path

    return df
