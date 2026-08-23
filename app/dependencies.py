from fastapi import Depends

from app.database import SessionLocal
from app.repositories import CategoryRepository, UserRepository
from app.services import CategoryService, UserService


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
