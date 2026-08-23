from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_product_image_service
from app.exceptions import NotFoundError
from app.schemas import (
    ProductImageCreate,
    ProductImageRead,
    ProductImageUpdate,
)
from app.services import ProductImageService

router = APIRouter(
    prefix="/product-images",
    tags=["Product Images"],
)


@router.post(
    "/",
    response_model=ProductImageRead,
    status_code=status.HTTP_201_CREATED,
)
def create(
    image_data: ProductImageCreate,
    image_service: ProductImageService = Depends(get_product_image_service),
):
    try:
        return image_service.create(image_data)

    except NotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


@router.get(
    "/product/{product_id}",
    response_model=list[ProductImageRead],
    status_code=status.HTTP_200_OK,
)
def get_images_by_product(
    product_id: int,
    image_service: ProductImageService = Depends(get_product_image_service),
):
    try:
        return image_service.get_all_by_product_id(product_id)

    except NotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


@router.get(
    "/{id}",
    response_model=ProductImageRead,
    status_code=status.HTTP_200_OK,
)
def get_by_id(
    id: int,
    image_service: ProductImageService = Depends(get_product_image_service),
):
    try:
        return image_service.get_by_id(id)

    except NotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


@router.patch(
    "/{id}",
    response_model=ProductImageRead,
    status_code=status.HTTP_200_OK,
)
def update(
    id: int,
    image_data: ProductImageUpdate,
    image_service: ProductImageService = Depends(get_product_image_service),
):
    try:
        return image_service.update(id, image_data)

    except NotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


@router.delete(
    "/{id}",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
def delete(
    id: int,
    image_service: ProductImageService = Depends(get_product_image_service),
):
    try:
        return image_service.delete(id)

    except NotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )
