from fastapi import Depends

from app.database import SessionLocal
from app.services import UserService
from app.repositories import UserRepository


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_user_service(session = Depends(get_session)):
    user_repository = UserRepository(session)
    return UserService(user_repository, session)

