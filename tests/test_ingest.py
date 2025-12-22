import pandas as pd
import numpy as np

from ingest import validate_schema, clean_data, normalize_features, process_file


def sample_telemetry_df():
    return pd.DataFrame({
        "vehicle_id": ["V1", "V2", "V1", None],
        "timestamp": ["2021-01-01 10:00", "2021-01-02 11:00", "2021-01-01 10:00", "bad"],
        "mileage_km": [1000, 1500, 1000, -10],
        "trip_distance_km": [10, 20, 10, 5],
    })


def test_validate_schema_passes():
    df = sample_telemetry_df()
    ok, missing = validate_schema(df)
    assert ok is True
    assert missing == []


def test_clean_data_and_normalize(tmp_path):
    df = sample_telemetry_df()
    cleaned = clean_data(df)
    # rows with missing vehicle_id or bad timestamps are removed
    assert cleaned["vehicle_id"].isna().sum() == 0
    assert cleaned.shape[0] >= 1

    normalized = normalize_features(cleaned, method="zscore")
    num_cols = cleaned.select_dtypes(include=[np.number]).columns.tolist()
    for c in num_cols:
        assert c + "_z" in normalized.columns


def test_process_file_writes_and_returns(tmp_path):
    df = sample_telemetry_df()
    inp = tmp_path / "in.csv"
    outp = tmp_path / "out.csv"
    df.to_csv(inp, index=False)

    res = process_file(str(inp), str(outp), normalize_method="minmax")
    assert str(outp) == res
    outdf = pd.read_csv(outp)
    assert outdf.shape[0] > 0
