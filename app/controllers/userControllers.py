import os
from sqlalchemy.orm import Session
from fastapi import Response

from app.models.User import Users
from app.utils.auth import hash_password, sign_token

from app.models.User import Users
from app.utils.auth import verify_password, sign_token

def create_user(db: Session, body: dict, response: Response):
    first_name = body.get("firstName")
    last_name = body.get("lastName")
    email = body.get("email")
    password = body.get("password")

    if not first_name or not last_name or not password:
        return {"error": "firstName, lastName, and password are required"}

    hashed = hash_password(password)

    user = Users(
        first_name=first_name,
        last_name=last_name,
        email = email,
        password=hashed
    )

    db.add(user)
    db.commit()
    db.refresh(user)

   
    token = sign_token({
        "firstName": user.first_name,
        "lastName": user.last_name,
        "id": user.id
    })


    node_env = os.getenv("NODE_ENV", "development")
    secure_cookie = (node_env == "production")  

    response.set_cookie(
        key="userAuth",
        value=token,
        httponly=True,
        secure=secure_cookie,
        samesite="lax"
    )

    return {"message": "success", "isLoggedIn": True, "userId": user.id}


def login_user(db: Session, body: dict, response: Response):
    first_name = body.get("firstName")
    last_name = body.get("lastName")
    email = body.get("email")
    password = body.get("password")

    if not first_name or not last_name or not email or not password:
        return {"error": "firstName, lastName, and password are required"}

    user = (
        db.query(Users)
        .filter(Users.first_name == first_name, Users.last_name == last_name)
        .first()
    )

    if not user:
        return {"error": "Invalid credentials"}

    if not verify_password(password, user.password):
        return {"error": "Invalid credentials"}

    token = sign_token({
        "firstName": user.first_name,
        "lastName": user.last_name,
        "email": user.email,
        "id": user.id
    })

    node_env = os.getenv("NODE_ENV", "development")
    secure_cookie = (node_env == "production")

    response.set_cookie(
        key="userAuth",
        value=token,
        httponly=True,
        secure=secure_cookie,
        samesite="lax"
    )

    return {"message": "success", "isLoggedIn": True}

