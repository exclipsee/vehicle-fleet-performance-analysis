import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import ElasticNetCV


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create derived features used by the dashboard and models.

    - Avg Trip Distance
    - Fuel per Trip
    - Maintenance per km
    - Month cyclic features
    """
    df = df.copy()
    df["Total Trips"] = df.get("Total Trips").replace(0, np.nan) if "Total Trips" in df else df.get("Total Trips")
    df["Avg Trip Distance (km)"] = df.get("Mileage (km)") / df.get("Total Trips")
    df["Fuel per Trip (L)"] = df.get("Fuel Used (L)") / df.get("Total Trips")
    df["Maintenance per km (€)"] = df.get("Maintenance Cost (€)") / df.get("Mileage (km)")
    # Month may be a string; try to parse
    if "Month" in df:
        try:
            df["Month_Num"] = pd.to_datetime(df["Month"], errors="coerce").dt.month
        except Exception:
            df["Month_Num"] = np.nan
    else:
        df["Month_Num"] = np.nan

    df["Month_sin"] = np.sin(2 * np.pi * (df["Month_Num"].fillna(0) / 12))
    df["Month_cos"] = np.cos(2 * np.pi * (df["Month_Num"].fillna(0) / 12))

    # sensible fills
    if "Avg Trip Distance (km)" in df:
        df["Avg Trip Distance (km)"] = df["Avg Trip Distance (km)"].fillna(df["Avg Trip Distance (km)"].median(skipna=True))
    if "Fuel per Trip (L)" in df:
        df["Fuel per Trip (L)"] = df["Fuel per Trip (L)"].fillna(df["Fuel per Trip (L)"].median(skipna=True))
    if "Maintenance per km (€)" in df:
        df["Maintenance per km (€)"] = df["Maintenance per km (€)"].fillna(0)

    return df


def split_numeric_categorical(X):
    numeric_feats = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_feats = [c for c in X.columns if c not in numeric_feats]
    return numeric_feats, categorical_feats


def build_pipeline(numeric_feats, categorical_feats):
    numeric_transformer = Pipeline(steps=[("scaler", StandardScaler())])
    # OneHotEncoder parameter name changed between sklearn versions.
    # Use `sparse_output=False` where available, fallback to `sparse=False`.
    try:
        ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        ohe = OneHotEncoder(handle_unknown="ignore", sparse=False)
    categorical_transformer = Pipeline(steps=[("onehot", ohe)])

    preprocessor = ColumnTransformer(transformers=[
        ("num", numeric_transformer, numeric_feats),
        ("cat", categorical_transformer, categorical_feats)
    ], remainder="drop")

    model = Pipeline(steps=[
        ("preproc", preprocessor),
        ("clf", ElasticNetCV(l1_ratio=[0.1, 0.5, 0.9], cv=3, n_alphas=10, random_state=42))
    ])

    return model
