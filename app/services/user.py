from app.exceptions import NotFoundError, UniqueFieldError
from app.utils.security import get_password_hash


class UserService:
    def __init__(self, user_repository, session):
        self.user_repository = user_repository
        self.session = session

    def create(self, user_data):
        user = self.user_repository.get_by_email(user_data.email)
        if user:
            raise UniqueFieldError("E-mail já cadastrado")

        hashed_password = get_password_hash(user_data.password)
        user_data.password = hashed_password

        return self.user_repository.create(user_data)

    def get_all(self):
        return self.user_repository.get_all()

    def get_by_id(self, id):
        user = self.user_repository.get_by_id(id)

        if not user:
            raise NotFoundError("Usuário não encontrado")

        return self.user_repository.get_by_id(id)

    def update(self, id, user_data):
        user = self.user_repository.get_by_id(id)

        if not user:
            raise NotFoundError("Usuário não encontrado")

        return self.user_repository.update(user, user_data)

    def delete(self, id):
        user = self.user_repository.get_by_id(id)

        if not user:
            raise NotFoundError("Usuário não encontrado")

        return self.user_repository.delete(user)
