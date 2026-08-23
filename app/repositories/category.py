from sqlalchemy.exc import IntegrityError

from app.exceptions import UniqueFieldError
from app.models import Category


class CategoryRepository:
    def __init__(self, session):
        self.session = session

    def create(self, category_data):
        category_db = Category(name=category_data.name)

        self.session.add(category_db)

        try:
            self.session.commit()
            self.session.refresh(category_db)

            return category_db

        except IntegrityError:
            self.session.rollback()

            raise UniqueFieldError("Categoria já cadastrada")

    def get_all(self):
        return self.session.query(Category).all()

    def get_by_id(self, id):
        return self.session.query(Category).filter(Category.id == id).first()

    def get_all_by_name(self, name):
        return (
            self.session.query(Category).filter(Category.name.ilike(f"%{name}%")).all()
        )

    def update(self, category, category_data):
        updated_data = {}

        for k, v in category_data.model_dump(exclude_unset=True).items():
            if v is not None:
                updated_data[k] = v

        db_fields = set(c.name for c in category.__table__.columns)

        for k, v in updated_data.items():
            if k in db_fields:
                setattr(category, k, v)

        try:
            self.session.commit()
            self.session.refresh(category)

            return category

        except IntegrityError:
            self.session.rollback()

            raise UniqueFieldError("Categoria já cadastrada")

    def delete(self, category):
        self.session.delete(category)
        self.session.commit()
