import pandas as pd
import numpy as np

from model_utils import engineer_features, split_numeric_categorical, build_pipeline


def sample_df():
    return pd.DataFrame({
        "Mileage (km)": [100, 200, 150, 120],
        "Total Trips": [2, 4, 3, 2],
        "Month": ["2021-01-01", "2021-06-01", "2021-12-01", "2021-03-01"],
        "Brand": ["A", "B", "A", "C"],
    })


def test_engineer_features_creates_columns():
    df = sample_df()
    out = engineer_features(df)
    assert "Avg Trip Distance (km)" in out.columns
    assert "Month_sin" in out.columns and "Month_cos" in out.columns


def test_split_numeric_categorical():
    df = sample_df()
    out = engineer_features(df)
    X = out[["Avg Trip Distance (km)", "Brand", "Month_sin"]]
    num, cat = split_numeric_categorical(X)
    assert "Avg Trip Distance (km)" in num
    assert "Brand" in cat


def test_pipeline_fit_predict():
    df = sample_df()
    out = engineer_features(df)
    X = out[["Avg Trip Distance (km)", "Month_sin", "Brand"]]
    y = out["Mileage (km)"]
    num, cat = split_numeric_categorical(X)
    model = build_pipeline(num, cat)
    model.fit(X, y)
    preds = model.predict(X)
    assert preds.shape[0] == X.shape[0]
    assert np.isfinite(preds).all()
