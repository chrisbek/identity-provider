from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.src.business_logic.exception.exceptions import ResourceAlreadyExists
from app.src.business_logic.model.user import User
from app.src.business_logic.services.logger_service import Logger
from app.src.business_logic.services.user_repository_interface import UserRepositoryInterface


class UserRepository(UserRepositoryInterface):
    def __init__(self, session: Session, logger: Logger):
        self.session = session
        self.logger = logger

    def count_users(self):
        return self.session.query(User).count()

    def create_or_update_user(self, user: User) -> User:
        try:
            self.session.add(user)
            self.session.flush()
            self.session.commit()
        except IntegrityError as e:
            raise ResourceAlreadyExists(f"User {user.external_identifier} already exists")

        return user

    def create_user(self, user: User) -> User:
        try:
            self.session.add(user)
            self.session.flush()
            self.session.commit()
        except IntegrityError as e:
            raise ResourceAlreadyExists(f"User {user.external_identifier} already exists")

        return user

    def find_user_by_external_identifier(self, external_identifier: str) -> Optional[User]:
        return self.session.query(User).filter(User.external_identifier == external_identifier) \
            .first()
