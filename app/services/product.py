import math

from fastapi import HTTPException, status

from app.exceptions import ConflictError, NotFoundError, UnprocessableEntityError
from app.models import ProductImage, User
from app.repositories import (
    CategoryRepository,
    ProductImageRepository,
    ProductRepository,
)
from app.schemas import ProductImageCreate
from app.services.storage import delete_image, upload_base64_image, get_public_url


class ProductService:
    def __init__(
        self,
        repository: ProductRepository,
        category_repository: CategoryRepository,
        product_image_repository: ProductImageRepository,
        session,
    ):
        self.repository = repository
        self.category_repository = category_repository
        self.product_image_repository = product_image_repository
        self.session = session

    def create(self, product_data, current_user):
        category = self.category_repository.get_by_id(product_data.category_id)

        if category is None:
            raise NotFoundError("Categoria não encontrada")

        if category.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para cadastrar o produto com esta categoria",
            )

        cover_count = sum(getattr(image, "is_cover", False) for image in product_data.images)
        if cover_count > 1:
            raise ConflictError("Um produto não pode ter mais de uma imagem de capa")

        uploaded_paths = []
        try:
            product = self.repository.create(
                product_data,
                current_user.id,
                commit=False,
            )
            self.session.flush()

            for image_data in product_data.images:
                path = upload_base64_image(
                    image_base64=image_data.url,
                    product_id=product.id,
                )
                uploaded_paths.append(path)

                image = ProductImageCreate(
                    product_id=product.id,
                    url=path,
                    is_cover=image_data.is_cover,
                )

                self.product_image_repository.create(
                    image,
                    commit=False,
                )

            self.session.commit()
            self.session.refresh(product)

            return product

        except Exception:
            self.session.rollback()
            for path in uploaded_paths:
                delete_image(path)
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

        if min_price is not None and max_price is not None and min_price > max_price:
            raise UnprocessableEntityError(
                "Preço mínimo não pode ser maior que o preço máximo"
            )

        if min_stock is not None and min_stock < 0:
            raise UnprocessableEntityError("Estoque mínimo não pode ser negativo")

        if max_stock is not None and max_stock < 0:
            raise UnprocessableEntityError("Estoque máximo não pode ser negativo")

        if min_stock is not None and max_stock is not None and min_stock > max_stock:
            raise UnprocessableEntityError(
                "Estoque mínimo não pode ser maior que o estoque máximo"
            )

        products, total_items = self.repository.get_all(
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

        return {
            "total_pages": math.ceil(total_items / page_size) if page_size > 0 else 0,
            "total_items": total_items,
            "products": products,
        }

    def get_my_products(
        self,
        current_user: User,
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

        if min_price is not None and max_price is not None and min_price > max_price:
            raise UnprocessableEntityError(
                "Preço mínimo não pode ser maior que o preço máximo"
            )

        if min_stock is not None and min_stock < 0:
            raise UnprocessableEntityError("Estoque mínimo não pode ser negativo")

        if max_stock is not None and max_stock < 0:
            raise UnprocessableEntityError("Estoque máximo não pode ser negativo")

        if min_stock is not None and max_stock is not None and min_stock > max_stock:
            raise UnprocessableEntityError(
                "Estoque mínimo não pode ser maior que o estoque máximo"
            )

        products, total_items = self.repository.get_all(
            user_id=current_user.id,
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

        return {
            "total_pages": math.ceil(total_items / page_size) if page_size > 0 else 0,
            "total_items": total_items,
            "products": products,
        }

    def get_by_id(self, id):
        product = self.repository.get_by_id(id)

        if product is None:
            raise NotFoundError("Produto não encontrado")

        return product

    def update(
        self,
        id,
        product_data,
        current_user,
    ):
        product = self.repository.get_by_id(id)

        if product is None:
            raise NotFoundError("Produto não encontrado")

        if product.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar este produto",
            )

        try:
            category = self.category_repository.get_by_id(product_data.category_id)
            if category is None:
                raise NotFoundError("Categoria não encontrada")

            if category.user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Você não tem permissão para atualizar o produto com esta categoria",
                )

            product.title = product_data.title
            product.description = product_data.description
            product.price = product_data.price
            product.stock = product_data.stock
            product.category_id = product_data.category_id
            product.is_visible = product_data.is_visible

            if product_data.images is not None:
                self._sync_product_images(product, product_data.images)

            self.session.commit()
            self.session.refresh(product)

            return product

        except Exception:
            self.session.rollback()
            raise

    def delete(self, id, current_user):
        product = self.repository.get_by_id(id)

        if product is None:
            raise NotFoundError("Produto não encontrado")

        if product.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para deletar este produto",
            )

        try:
            for img in product.images:
                delete_image(img.url)

            self.repository.delete(product)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            raise

    def _sync_product_images(self, product, incoming_images):
        cover_count = sum(1 for img in incoming_images if getattr(img, "is_cover", False))
        if cover_count > 1:
            raise ConflictError("Um produto não pode ter mais de uma imagem de capa")

        incoming_ids = set()
        incoming_urls = set()  # fallback pra casar por url quando o id não vier

        for img in incoming_images:
            img_id = getattr(img, "id", None)
            if img_id is not None:
                try:
                    incoming_ids.add(int(img_id))
                except (ValueError, TypeError):
                    pass

            raw_url = getattr(img, "url", "") or ""
            if raw_url and not raw_url.startswith("data:"):
                incoming_urls.add(raw_url)

        # Só remove se NEM o id NEM a url baterem com algo que veio no payload
        images_to_remove = [
            img for img in product.images
            if img.id not in incoming_ids and get_public_url(img.url) not in incoming_urls
        ]
        for img in images_to_remove:
            delete_image(img.url)
            product.images.remove(img)
            self.session.delete(img)

        self.session.flush()

        # Reseta as capas
        for img in product.images:
            img.is_cover = False

        current_images_map = {img.id: img for img in product.images}

        for img_data in incoming_images:
            img_id = getattr(img_data, "id", None)
            if img_id is not None:
                try:
                    img_id = int(img_id)
                except (ValueError, TypeError):
                    img_id = None

            is_cover = bool(getattr(img_data, "is_cover", False))
            raw_url = getattr(img_data, "url", "") or ""

            # Caso 1: Imagem existente no banco
            if img_id is not None and img_id in current_images_map:
                existing_image = current_images_map[img_id]
                existing_image.is_cover = is_cover

                # Se o usuário substituiu o arquivo por um Base64 novo
                if raw_url.startswith("data:"):
                    delete_image(existing_image.url)
                    new_path = upload_base64_image(
                        image_base64=raw_url,
                        product_id=product.id,
                    )
                    existing_image.url = new_path

            # Caso 2: Imagem Nova
            else:
                if raw_url.startswith("data:"):
                    path = upload_base64_image(
                        image_base64=raw_url,
                        product_id=product.id,
                    )
                    new_image = ProductImage(
                        url=path,
                        product_id=product.id,
                        is_cover=is_cover,
                    )
                    product.images.append(new_image)