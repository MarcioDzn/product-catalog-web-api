from fastapi import FastAPI

from app.routes import (
    auth_router,
    category_router,
    product_image_router,
    product_router,
    user_router,
)

app = FastAPI()

app.include_router(user_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(product_image_router)
app.include_router(auth_router)


@app.get("/")
def home():
    return {"message": "Hello World"}
