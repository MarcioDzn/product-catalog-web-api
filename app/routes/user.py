from app.exceptions import NotFoundError, UniqueFieldError
from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_user_service
from app.schemas import UserCreate, UserRead, UserUpdate
from app.services import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create(
    user_data: UserCreate, user_service: UserService = Depends(get_user_service)
):
    try:
        return user_service.create(user_data)
    except UniqueFieldError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="E-mail já cadastrado"
        )


@router.get("/", response_model=list[UserRead], status_code=status.HTTP_200_OK)
def get_users(user_service: UserService = Depends(get_user_service)):
    return user_service.get_all()


@router.get("/{id}", response_model=UserRead, status_code=status.HTTP_200_OK)
def get_user_by_id(id: int, user_service: UserService = Depends(get_user_service)):
    try:
        return user_service.get_by_id(id)
    except NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.patch("/{id}", response_model=UserRead, status_code=status.HTTP_200_OK)
def update_user(
    id: int,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service),
):
    try:
        return user_service.update(id, user_data)
    except NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except UniqueFieldError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))


@router.delete("/{id}", response_model=None, status_code=status.HTTP_200_OK)
def delete_user(id: int, user_service: UserService = Depends(get_user_service)):
    try:
        return user_service.delete(id)
    except NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
