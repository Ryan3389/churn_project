from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.config.connection import get_db
from app.controllers.userControllers import create_user
from app.controllers.userControllers import create_user, login_user
from app.utils.auth import require_auth

router = APIRouter()

@router.post("/createUser")
def create_user_route(payload: dict, response: Response, db: Session = Depends(get_db)):
    return create_user(db=db, body=payload, response=response)


@router.post("/login")
def login_route(payload: dict, response: Response, db: Session = Depends(get_db)):
    return login_user(db=db, body=payload, response=response)

@router.get("/me")
def me_route(user_data: dict = Depends(require_auth)):
    return {"authenticated": True, "user": user_data}