from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import (
    auth_router,
    category_router,
    product_image_router,
    product_router,
    user_router,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(product_image_router)
app.include_router(auth_router)


@app.get("/")
def home():
    return {"message": "Hello World"}
