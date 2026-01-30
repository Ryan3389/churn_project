from fastapi import APIRouter
from app.controllers.predictControllers import predict_controller

router = APIRouter()

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.connection import get_db
from app.utils.auth import require_auth
from app.models.User import Users
from app.ML.model import run_prediction  

router = APIRouter()

@router.post("/predict")
def predict_and_save(
    payload: dict,
    db: Session = Depends(get_db),
    user_data: dict = Depends(require_auth)  
):
    prediction = run_prediction(payload)

    user_id = user_data["id"]
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    
    user.predictions.append(float(prediction))
    db.commit()
    db.refresh(user)

    return {
        "prediction": int(prediction),
        "saved": True,
        "total_predictions": len(user.predictions)
    }



