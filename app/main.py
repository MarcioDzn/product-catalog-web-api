from fastapi import FastAPI

from app.routes import category_router, user_router, product_router

app = FastAPI()

app.include_router(user_router)
app.include_router(category_router)
app.include_router(product_router)


@app.get("/")
def home():
    return {"message": "Hello World"}
