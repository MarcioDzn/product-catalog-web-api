from app.models import ProductImage


class ProductImageRepository:
    def __init__(self, session):
        self.session = session

    def create(self, product_image_data):
        product_image_db = ProductImage(
            product_id=product_image_data.product_id,
            url=product_image_data.url,
            is_cover=product_image_data.is_cover,
        )

        self.session.add(product_image_db)
        self.session.commit()
        self.session.refresh(product_image_db)

        return product_image_db

    def get_all_by_product_id(self, product_id):
        return (
            self.session.query(ProductImage)
            .filter(ProductImage.product_id == product_id)
            .all()
        )

    def get_cover_by_product_id(self, product_id):
        return (
            self.session.query(ProductImage)
            .filter(
                ProductImage.product_id == product_id,
                ProductImage.is_cover.is_(True),
            )
            .first()
        )
    
    def unset_cover(self, image):
        image.is_cover = False
        self.session.flush()

    def get_by_id(self, id):
        return self.session.query(ProductImage).filter(ProductImage.id == id).first()

    def update(self, product_image, product_image_data):
        updated_data = {}

        for key, value in product_image_data.model_dump(exclude_unset=True).items():
            if value is not None:
                updated_data[key] = value

        db_fields = {column.name for column in product_image.__table__.columns}

        for key, value in updated_data.items():
            if key in db_fields:
                setattr(product_image, key, value)

        self.session.commit()
        self.session.refresh(product_image)

        return product_image

    def delete(self, product_image):
        self.session.delete(product_image)
        self.session.commit()
