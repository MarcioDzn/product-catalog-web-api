from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProductImageBase(BaseModel):
    url: str
    product_id: int


class ProductImageCreate(ProductImageBase):
    is_cover: bool = False


class ProductImageUpdate(BaseModel):
    id: Optional[int] = None
    url: str
    is_cover: bool


class ProductImageRead(ProductImageBase):
    id: int
    is_cover: bool

    model_config = ConfigDict(from_attributes=True)
