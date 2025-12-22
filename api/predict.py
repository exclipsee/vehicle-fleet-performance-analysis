from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import os
import joblib
import pandas as pd

app = FastAPI(title="Fleet Model API")


class PredictRequest(BaseModel):
    features: List[Dict[str, Any]]


MODEL_PATH = os.environ.get("MODEL_PATH", "saved_models/latest_model.joblib")
_model = None


def load_model(path: str):
    global _model
    if os.path.exists(path):
        _model = joblib.load(path)
    else:
        _model = None


@app.on_event("startup")
def startup_event():
    load_model(MODEL_PATH)


@app.get("/status")
def status():
    return {"model_loaded": _model is not None, "model_path": MODEL_PATH}


@app.post("/predict")
def predict(req: PredictRequest):
    if _model is None:
        raise HTTPException(status_code=503, detail="Model not available. Train and place model at 'saved_models/latest_model.joblib'.")
    try:
        df = pd.DataFrame(req.features)
        preds = _model.predict(df)
        return {"predictions": preds.tolist()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
