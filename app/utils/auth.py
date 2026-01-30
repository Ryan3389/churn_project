import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import bcrypt
from jose import jwt, JWTError
from fastapi import Request, HTTPException, status


load_dotenv()

SECRET = os.getenv("SECRET", "dev_secret")
EXPIRATION = os.getenv("EXPIRATION", "2h")


def hash_password(password: str) -> str:
    # bcrypt expects bytes
    salt = bcrypt.gensalt(rounds=10)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def _parse_expiration(exp: str) -> timedelta:
    exp = exp.strip().lower()
    if exp.endswith("h"):
        return timedelta(hours=int(exp[:-1]))
    if exp.endswith("m"):
        return timedelta(minutes=int(exp[:-1]))
    if exp.endswith("d"):
        return timedelta(days=int(exp[:-1]))
    return timedelta(seconds=int(exp))


def sign_token(payload: dict) -> str:
    expires_delta = _parse_expiration(EXPIRATION)
    to_encode = {"data": payload, "exp": datetime.utcnow() + expires_delta}
    return jwt.encode(to_encode, SECRET, algorithm="HS256")


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        data = payload.get("data")
        if not data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        return data
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

def require_auth(request: Request) -> dict:
    """
    FastAPI dependency that:
    - reads JWT from 'userAuth' cookie
    - validates it
    - returns the decoded user data
    """
    token = request.cookies.get("userAuth")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return decode_token(token)