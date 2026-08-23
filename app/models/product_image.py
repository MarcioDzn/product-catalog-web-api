from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Index
from sqlalchemy.orm import relationship

from app.database import Base


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    url = Column(String(500), nullable=False)
    is_cover = Column(Boolean, nullable=False, default=False)

    product = relationship("Product", back_populates="images")

    __table_args__ = (
        Index(
            "uq_product_cover",
            "product_id",
            unique=True,
            postgresql_where=(is_cover == True)
        ),
    )