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
    return {"status": "online", "message": "My JWT API is running"}

@app.post("/token")
def create_token(data: TokenRequest):
    if not SECRET_KEY:
        raise HTTPException(status_code=500, detail="JWT_SECRET_KEY is not configured")
    
    payload = {
        "sub": data.user_id,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

