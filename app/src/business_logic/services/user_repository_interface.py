from typing import Optional
from app.src.business_logic.model.user import User


class UserRepositoryInterface:
    def create_or_update_user(self, user: User) -> User:
        pass

    def create_user(self, user: User) -> User:
        pass

    def find_user_by_external_identifier(self, external_identifier: str) -> Optional[User]:
        pass
