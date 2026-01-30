from app.ML.model import run_prediction

def predict_controller(body: dict):
    prediction = run_prediction(body)
    return {"prediction": prediction}
