from app.exceptions import ConflictError, NotFoundError, UnprocessableEntityError
from app.repositories import (
    CategoryRepository,
    ProductImageRepository,
    ProductRepository,
)
from app.schemas import ProductImageCreate


class ProductService:
    def __init__(
        self,
        repository: ProductRepository,
        category_repository: CategoryRepository,
        product_image_repository: ProductImageRepository,
    ):
        self.repository = repository
        self.category_repository = category_repository
        self.product_image_repository = product_image_repository

    def create(self, product_data):
        category = self.category_repository.get_by_id(product_data.category_id)

        if category is None:
            raise NotFoundError("Categoria não encontrada")

        cover_count = sum(image.is_cover for image in product_data.images)
        if cover_count > 1:
            raise ConflictError("Um produto não pode ter mais de uma imagem de capa")

        try:
            product = self.repository.create(
                product_data,
                commit=False,
            )

            for image_data in product_data.images:
                image = ProductImageCreate(
                    product_id=product.id,
                    url=image_data.url,
                    is_cover=image_data.is_cover,
                )

                self.product_image_repository.create(
                    image,
                    commit=False,
                )

            self.repository.session.commit()
            self.repository.session.refresh(product)

            return product
        except Exception:
            self.repository.session.rollback()
            raise

    def get_all(
        self,
        title: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        min_stock: int | None = None,
        max_stock: int | None = None,
        sort: str | None = None,
        category_ids: list[int] | None = None,
        page: int = 1,
        page_size: int = 20,
    ):

        if min_price is not None and min_price < 0:
            raise UnprocessableEntityError("Preço mínimo não pode ser negativo")

        if max_price is not None and max_price < 0:
            raise UnprocessableEntityError("Preço máximo não pode ser negativo")

        if min_price is not None and max_price is not None:
            if min_price > max_price:
                raise UnprocessableEntityError(
                    "Preço mínimo não pode ser maior que o preço máximo"
                )

        if min_stock is not None and min_stock < 0:
            raise UnprocessableEntityError("Estoque mínimo não pode ser negativo")

        if max_stock is not None and max_stock < 0:
            raise UnprocessableEntityError("Estoque máximo não pode ser negativo")

        if min_stock is not None and max_stock is not None:
            if min_stock > max_stock:
                raise UnprocessableEntityError(
                    "Estoque mínimo não pode ser maior que o estoque máximo"
                )

        return self.repository.get_all(
            title=title,
            min_price=min_price,
            max_price=max_price,
            min_stock=min_stock,
            max_stock=max_stock,
            sort=sort,
            category_ids=category_ids,
            page=page,
            page_size=page_size,
        )

    def get_by_id(self, id):
        product = self.repository.get_by_id(id)

        if product is None:
            raise NotFoundError("Produto não encontrado")

        return product

    def update(self, id, product_data):
        product = self.get_by_id(id)

        return self.repository.update(product, product_data)

    def delete(self, id):
        product = self.get_by_id(id)

        return self.repository.delete(product)
