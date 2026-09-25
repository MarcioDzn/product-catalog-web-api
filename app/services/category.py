from fastapi import HTTPException, status

from app.exceptions import NotFoundError, UniqueFieldError
from app.repositories import CategoryRepository


class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def create(self, category_data, current_user):
        existing_category = self.repository.get_all_by_name(category_data.name)

        if existing_category:
            raise UniqueFieldError("Categoria já cadastrada")

        return self.repository.create(
            category_data, 
            current_user.id
        )

    def get_all(self, name):
        if name:
            return self.repository.get_all_by_name(name)
        return self.repository.get_all()

    def get_my_categories(self, name, current_user):
        if name:
            return self.repository.get_all_by_name(name, current_user.id)
        return self.repository.get_all(current_user.id)

    def get_by_id(self, id):
        category = self.repository.get_by_id(id)

        if category is None:
            raise NotFoundError("Categoria não encontrada")

        return category

    def get_all_by_name(self, name):
        return self.repository.get_all_by_name(name)

    def update(self, id, category_data, current_user):
        category = self.get_by_id(id)

        if category is None:
            raise NotFoundError("Categoria não encontrada")

        if category.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar este produto",
            )
    

        if category_data.name is not None:
            existing_category = self.repository.get_all_by_name(category_data.name)

            if existing_category and existing_category.id != category.id:
                raise UniqueFieldError("Categoria já cadastrada")

        return self.repository.update(category, category_data)

    def delete(self, id, current_user):
        category = self.get_by_id(id)

        if category is None:
            raise NotFoundError("Categoria não encontrada")

        if category.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar este produto",
            )

        return self.repository.delete(category)
