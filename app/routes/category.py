from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_category_service
from app.exceptions import NotFoundError, UniqueFieldError
from app.schemas import CategoryCreate, CategoryRead, CategoryUpdate
from app.services import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create(
    category_data: CategoryCreate,
    category_service: CategoryService = Depends(get_category_service),
):
    try:
        return category_service.create(category_data)
    except UniqueFieldError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))


@router.get("/", response_model=list[CategoryRead], status_code=status.HTTP_200_OK)
def get_categories(name: str | None = None, category_service: CategoryService = Depends(get_category_service)):
    return category_service.get_all(name)


@router.get("/{id}", response_model=CategoryRead, status_code=status.HTTP_200_OK)
def get_category_by_id(
    id: int, category_service: CategoryService = Depends(get_category_service)
):
    try:
        return category_service.get_by_id(id)
    except NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.patch("/{id}", response_model=CategoryRead, status_code=status.HTTP_200_OK)
def update_category(
    id: int,
    category_data: CategoryUpdate,
    category_service: CategoryService = Depends(get_category_service),
):
    try:
        return category_service.update(id, category_data)
    except NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except UniqueFieldError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))


@router.delete("/{id}", response_model=None, status_code=status.HTTP_200_OK)
def delete_category(
    id: int, category_service: CategoryService = Depends(get_category_service)
):
    try:
        return category_service.delete(id)
    except NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
