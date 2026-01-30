import joblib
import pandas as pd

pipeline = joblib.load("churn_pipeline.pkl")

def run_prediction(data: dict) -> int:
    df = pd.DataFrame([data])
    prediction = pipeline.predict(df)[0]
    return int(prediction)
