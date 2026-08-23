from fastapi import FastAPI
from app.routes import user_router

app = FastAPI()

app.include_router(user_router)

@app.get("/")
def home():
    return {"message": "Hello World"}
