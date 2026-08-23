from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.product_image import ProductImageCreate, ProductImageRead


class ProductBase(BaseModel):
    category_id: int
    title: str
    description: Optional[str] = None
    price: Decimal
    is_visible: bool = True
    stock: int = 0


class ProductCreate(ProductBase):
    images: list[ProductImageCreate] = Field(default_factory=list)


class ProductUpdate(BaseModel):
    category_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    is_visible: Optional[bool] = None
    stock: Optional[int] = None


class ProductRead(ProductBase):
    id: int
    images: list[ProductImageRead] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)