from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator
from app.services.storage import get_public_url  


class ProductImageBase(BaseModel):
    url: str
    product_id: int


class ProductImageCreate(ProductImageBase):
    is_cover: bool = False


class ProductImageUpdate(BaseModel):
    id: Optional[int] = None
    url: str
    is_cover: bool = False


class ProductImageRead(ProductImageBase):
    id: int
    is_cover: bool

    model_config = ConfigDict(from_attributes=True)

    @field_validator("url", mode="after")
    @classmethod
    def assemble_public_url(cls, v: str) -> str:
        return get_public_url(v)