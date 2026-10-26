from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "My JWT API is running!"}
