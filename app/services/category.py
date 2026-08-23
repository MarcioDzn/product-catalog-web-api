from app.exceptions import NotFoundError, UniqueFieldError
from app.repositories import CategoryRepository


class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def create(self, category_data):
        existing_category = self.repository.get_all_by_name(category_data.name)

        if existing_category:
            raise UniqueFieldError("Categoria já cadastrada")

        return self.repository.create(category_data)

    def get_all(self, name):
        if name:
            return self.repository.get_all_by_name(name)
        return self.repository.get_all()

    def get_by_id(self, id):
        category = self.repository.get_by_id(id)

        if category is None:
            raise NotFoundError("Categoria não encontrada")

        return category

    def get_all_by_name(self, name):
        return self.repository.get_all_by_name(name)

    def update(self, id, category_data):
        category = self.get_by_id(id)

        if category_data.name is not None:
            existing_category = self.repository.get_all_by_name(category_data.name)

            if existing_category and existing_category.id != category.id:
                raise UniqueFieldError("Categoria já cadastrada")

        return self.repository.update(category, category_data)

    def delete(self, id):
        category = self.get_by_id(id)

        return self.repository.delete(category)
