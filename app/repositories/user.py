from sqlalchemy.exc import IntegrityError

from app.exceptions import UniqueFieldError
from app.models import User


class UserRepository:
    def __init__(self, session):
        self.session = session

    def create(self, user_data):
        user_db = User(
            name=user_data.name, email=user_data.email, password=user_data.password
        )

        self.session.add(user_db)

        try:
            self.session.commit()
            self.session.refresh(user_db)
            return user_db

        except IntegrityError:
            self.session.rollback()
            raise UniqueFieldError("E-mail já cadastrado")

    def get_all(self):
        return self.session.query(User).all()

    def get_by_id(self, id):
        return self.session.query(User).filter(User.id == id).first()

    def update(self, user, user_data):
        updated_data = {}
        for k, v in user_data.dict(exclude_unset=True).items():
            if v is not None:
                updated_data[k] = v

        db_fields = set(c.name for c in user.__table__.columns)

        for k, v in updated_data.items():
            if k in db_fields:
                setattr(user, k, v)

        self.session.commit()
        self.session.refresh(user)

        return user
    

    def delete(self, user):
        self.session.delete(user)
        self.session.commit()
