import pandas as pd
import numpy as np

from model_utils import engineer_features, split_numeric_categorical, build_pipeline


def make_sample_df():
    return pd.DataFrame({
        "Mileage (km)": [100, 200, 150, 0],
        "Fuel Used (L)": [10, 20, 15, 1],
        "Maintenance Cost (€)": [5, 10, 7.5, 0],
        "Total Trips": [2, 4, 3, 1],
        "Month": ["2021-01-01", "2021-06-01", "2021-12-01", None],
        "Brand": ["A", "B", "A", "C"],
        "Vehicle_Type": ["Van", "Truck", "Van", "Car"],
    })


def test_engineer_features_creates_columns():
    df = make_sample_df()
    out = engineer_features(df)
    assert "Avg Trip Distance (km)" in out.columns
    assert "Fuel per Trip (L)" in out.columns
    assert "Maintenance per km (€)" in out.columns
    assert "Month_sin" in out.columns and "Month_cos" in out.columns


def test_split_numeric_categorical():
    df = make_sample_df()
    out = engineer_features(df)
    X = out[["Avg Trip Distance (km)", "Brand", "Month_sin"]]
    num, cat = split_numeric_categorical(X)
    assert "Avg Trip Distance (km)" in num
    assert "Brand" in cat


def test_pipeline_fit_predict():
    df = make_sample_df()
    out = engineer_features(df)
    X = out[["Avg Trip Distance (km)", "Fuel per Trip (L)", "Brand"]]
    y = out["Mileage (km)"]
    num, cat = split_numeric_categorical(X)
    model = build_pipeline(num, cat)
    model.fit(X, y)
    preds = model.predict(X)
    assert preds.shape[0] == X.shape[0]
    # predictions should be finite numbers
    assert np.isfinite(preds).all()
