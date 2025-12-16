import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import ElasticNetCV


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Average trip distance (simple)
    if "Total Trips" in df:
        trips = df["Total Trips"].replace(0, np.nan)
    else:
        trips = pd.Series(np.nan, index=df.index)
    df["Avg Trip Distance (km)"] = df.get("Mileage (km)", 0) / trips

    # Month numeric and cyclic encode
    if "Month" in df:
        df["Month_Num"] = pd.to_datetime(df["Month"], errors="coerce").dt.month
    else:
        df["Month_Num"] = np.nan
    df["Month_sin"] = np.sin(2 * np.pi * (df["Month_Num"].fillna(0) / 12))
    df["Month_cos"] = np.cos(2 * np.pi * (df["Month_Num"].fillna(0) / 12))

    df["Avg Trip Distance (km)"] = df["Avg Trip Distance (km)"].fillna(df["Avg Trip Distance (km)"].median(skipna=True))
    return df


def split_numeric_categorical(X: pd.DataFrame):
    numeric = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical = [c for c in X.columns if c not in numeric]
    return numeric, categorical


def build_pipeline(numeric_feats, categorical_feats):
    num_pipe = Pipeline([("scale", StandardScaler())])
    try:
        ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        ohe = OneHotEncoder(handle_unknown="ignore", sparse=False)
    cat_pipe = Pipeline([("ohe", ohe)])
    pre = ColumnTransformer([("num", num_pipe, numeric_feats), ("cat", cat_pipe, categorical_feats)], remainder="drop")
    pipe = Pipeline([("pre", pre), ("clf", ElasticNetCV(l1_ratio=[0.5], cv=3, n_alphas=10, random_state=42))])
    return pipe
