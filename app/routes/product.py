from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_product_service
from app.exceptions import NotFoundError, UniqueFieldError, UnprocessableEntityError
from app.schemas import ProductCreate, ProductRead, ProductUpdate
from app.services import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create(
    product_data: ProductCreate,
    product_service: ProductService = Depends(get_product_service),
):
    try:
        return product_service.create(product_data)

    except UniqueFieldError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))
    except NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.get("/", response_model=list[ProductRead], status_code=status.HTTP_200_OK)
def get_products(
    title: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    min_stock: int | None = None,
    max_stock: int | None = None,
    sort: str | None = None,
    product_service: ProductService = Depends(get_product_service),
):
    try:
        return product_service.get_all(
            title=title,
            min_price=min_price,
            max_price=max_price,
            min_stock=min_stock,
            max_stock=max_stock,
            sort=sort
        )

    except UnprocessableEntityError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)
        )

@router.get("/category/{category_id}", response_model=list[ProductRead], status_code=status.HTTP_200_OK)
def get_products_by_category(
    category_id: int,
    title: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    min_stock: int | None = None,
    max_stock: int | None = None,
    sort: str | None = None,
    product_service: ProductService = Depends(get_product_service),
):
    try:
        return product_service.get_all(
            title=title,
            min_price=min_price,
            max_price=max_price,
            min_stock=min_stock,
            max_stock=max_stock,
            sort=sort,
            category_id=category_id
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
