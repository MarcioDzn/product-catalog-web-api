from pydantic import BaseModel, ConfigDict


class ProductImageBase(BaseModel):
    url: str


class ProductImageCreate(ProductImageBase):
    is_cover: bool = False


class ProductImageUpdate(BaseModel):
    url: str | None = None


class ProductImageRead(ProductImageBase):
    id: int
    product_id: int
    is_cover: bool

    model_config = ConfigDict(from_attributes=True)