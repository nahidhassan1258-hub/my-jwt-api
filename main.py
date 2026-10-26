import os
from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)

API_PASSWORD = os.environ.get("API_PASSWORD")

def password_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not API_PASSWORD:
            return jsonify({
                "error": "Server password not configured"
            }), 500

        password = request.headers.get("X-API-Password")

        if password != API_PASSWORD:
            return jsonify({
                "error": "Wrong or missing password"
            }), 401

        return func(*args, **kwargs)
    return wrapper

@app.route("/")
def home():
    return jsonify({
        "status": "API is running"
    })

@app.route("/api/test", methods=["GET"])
@password_required
def test_api():
    return jsonify({
        "success": True,
        "message": "Password verified"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

python
fastapi import FastAPI
from pydantic import BaseModel
from jose import jwt, JWTError
import os
import time

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
        return {"error": "JWT_SECRET_KEY is not configured"}

    payload = {
        "sub": data.user_id,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/verify")
def verify_token(token: str):
    if not SECRET_KEY:
        return {"error": "JWT_SECRET_KEY is not configured"}

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"valid": True, "user_id": payload["sub"]}
    except JWTError:
        return {"valid": False, "message": "Invalid or expired token"}
