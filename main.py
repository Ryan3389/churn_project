# Main imports
from fastapi import FastAPI
import joblib
import pandas as pd
import uvicorn
import psycopg2

# Imports for auth
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from jose import jwt, JWTError
from passlib.context import CryptContext
# from database import init_db, get_user, create_user


app = FastAPI()

SECRET_KEY = "secret"          
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def init_db():
     conn = psycopg2.connect("dbname=churn_predict user=postgres password=postgres host=127.0.0.1 port=5432")
     conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            hashed_password TEXT NOT NULL,
            full_name TEXT
        )
    """)
     conn.commit()
     conn.close()




# Saved model pipeline
pipeline = joblib.load("churn_pipeline.pkl")

# Post request for making a prediction
@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])
    prediction = pipeline.predict(df)[0]
    return {"prediction": int(prediction)}



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)