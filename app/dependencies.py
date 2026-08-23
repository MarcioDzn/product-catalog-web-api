from fastapi import Depends

from app.database import SessionLocal
from app.repositories import (
    CategoryRepository,
    ProductImageRepository,
    ProductRepository,
    UserRepository,
)
from app.services import (
    CategoryService,
    ProductImageService,
    ProductService,
    UserService,
)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_user_service(session=Depends(get_session)):
    user_repository = UserRepository(session)
    return UserService(user_repository, session)


def get_category_service(session=Depends(get_session)):
    category_repository = CategoryRepository(session)
    return CategoryService(category_repository)


def get_product_service(session=Depends(get_session)):
    category_repository = CategoryRepository(session)
    product_repository = ProductRepository(session)
    product_image_repository = ProductImageRepository(session)
    return ProductService(
        product_repository, category_repository, product_image_repository
    )


def get_product_image_service(session=Depends(get_session)):
    product_repository = ProductRepository(session)
    product_image_repository = ProductImageRepository(session)
    return ProductImageService(product_image_repository, product_repository)
