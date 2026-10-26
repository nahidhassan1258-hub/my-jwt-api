
import os
import time

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from jose import jwt, JWTError

app = FastAPI(title="My JWT API")

SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = "HS256"


class TokenRequest(BaseModel):
    user_id: str


@app.get("/")
def home():
    return {"status": "API is running"}


@app.post("/token")
def create_token(data: TokenRequest):
    if not SECRET_KEY:
        raise HTTPException(
            status_code=500,
            detail="JWT_SECRET_KEY is not configured"
        )

    payload = {
        "sub": data.user_id,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600
    }

    token = jwt.encode(
        payload, SECRET_KEY, algorithm=ALGORITHM
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.post("/verify")
def verify_token(token: str):
    if not SECRET_KEY:
        raise HTTPException(
            status_code=500,
            detail="JWT_SECRET_KEY is not configured"
        )

    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        return {
            "valid": True,
            "user_id": payload["sub"]
        }
    except JWTError:
        return {
            "valid": False,
            "message": "Invalid or expired token"
        }

