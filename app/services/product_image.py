from app.exceptions import NotFoundError
from app.repositories import ProductImageRepository, ProductRepository


class ProductImageService:
    def __init__(
        self, repository: ProductImageRepository, product_repository: ProductRepository
    ):
        self.repository = repository
        self.product_repository = product_repository

    def create(self, image_data):
        product = self.product_repository.get_by_id(image_data.product_id)

        if not product:
            raise NotFoundError("Produto não encontrado")

        if image_data.is_cover:
            current_cover = self.repository.get_cover_by_product_id(
                image_data.product_id
            )

            if current_cover:
                self.repository.unset_cover(current_cover)

        return self.repository.create(image_data)

    def get_all_by_product_id(self, product_id):
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise NotFoundError("Produto não encontrado")
        
        return self.repository.get_all_by_product_id(product_id)

    def get_by_id(self, id):
        image = self.repository.get_by_id(id)

        if image is None:
            raise NotFoundError("Imagem não encontrada")

        return image

    def update(self, id, image_data):
        image = self.get_by_id(id)

        if image_data.is_cover is True:
            current_cover = self.repository.get_cover_by_product_id(image.product_id)

            if current_cover and current_cover.id != image.id:
                self.repository.unset_cover(current_cover)

        return self.repository.update(image, image_data)

    def delete(self, id):
        image = self.get_by_id(id)

        return self.repository.delete(image)
