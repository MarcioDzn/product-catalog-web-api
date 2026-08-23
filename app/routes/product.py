from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.auth import get_current_user, get_optional_current_user
from app.dependencies import get_product_service
from app.exceptions import (
    ConflictError,
    NotFoundError,
    UniqueFieldError,
    UnprocessableEntityError,
)
from app.models import User
from app.schemas import ProductCreate, ProductRead, ProductUpdate
from app.services import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create(
    product_data: ProductCreate,
    product_service: ProductService = Depends(get_product_service),
    current_user: User = Depends(get_current_user),
):
    try:
        return product_service.create(product_data)

    except UniqueFieldError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))
    except NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except ConflictError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))


# TODO: Adicionar verificação de auth
# Apenas usuários autenticados podem filtrar por is_visible
# Usuários não auth veem apenas visible=True
@router.get("/", response_model=list[ProductRead], status_code=status.HTTP_200_OK)
def get_products(
    title: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    min_stock: int | None = None,
    max_stock: int | None = None,
    sort: str | None = None,
    category_ids: Annotated[list[int] | None, Query()] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    product_service: ProductService = Depends(get_product_service),
    current_user: User | None = Depends(get_optional_current_user),
):
    try:
        return product_service.get_all(
            title=title,
            min_price=min_price,
            max_price=max_price,
            min_stock=min_stock,
            max_stock=max_stock,
            sort=sort,
            page=page,
            page_size=page_size,
            category_ids=category_ids,
        )

    except UnprocessableEntityError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)
        )


@router.get("/{id}", response_model=ProductRead, status_code=status.HTTP_200_OK)
def get_product_by_id(
    id: int, product_service: ProductService = Depends(get_product_service)
):
    try:
        return product_service.get_by_id(id)

    except NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.patch("/{id}", response_model=ProductRead, status_code=status.HTTP_200_OK)
def update_product(
    id: int,
    product_data: ProductUpdate,
    product_service: ProductService = Depends(get_product_service),
):
    try:
        return product_service.update(id, product_data)

    except NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))

    except UniqueFieldError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))


@router.delete("/{id}", response_model=None, status_code=status.HTTP_200_OK)
def delete_product(
    id: int, product_service: ProductService = Depends(get_product_service)
):
    try:
        return product_service.delete(id)

    except NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
