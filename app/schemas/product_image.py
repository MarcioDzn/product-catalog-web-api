from pydantic import BaseModel, ConfigDict


class ProductImageBase(BaseModel):
    url: str
    product_id: int


class ProductImageCreate(ProductImageBase):
    is_cover: bool = False


class ProductImageUpdate(BaseModel):
    url: str | None = None
    is_cover: bool | None = None


class ProductImageRead(ProductImageBase):
    id: int
    is_cover: bool

    model_config = ConfigDict(from_attributes=True)
