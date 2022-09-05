from typing import Optional, List
from app.src.business_logic.exception.exceptions import ResourceNotFound
from app.src.business_logic.model.role import Role
from app.src.business_logic.model.user import User
from app.src.business_logic.services.operation_repository_interface import OperationRepositoryInterface
from app.src.business_logic.services.resource_repository_interface import ResourceRepositoryInterface
from app.src.business_logic.services.role_repository_interface import RoleRepositoryInterface
from app.src.business_logic.services.user_repository_interface import UserRepositoryInterface
from app.src.business_logic.services.logger_service import Logger


class IdentityService:
    def __init__(
            self,
            logger: Logger,
            user_repo: UserRepositoryInterface,
            role_repo: RoleRepositoryInterface,
            resource_repo: ResourceRepositoryInterface,
            operation_repo: OperationRepositoryInterface,
    ):
        self.logger = logger
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.resource_repo = resource_repo
        self.operation_repo = operation_repo

    def find_user_from_external_identifier(self, external_identifier: str) -> Optional[User]:
        return self.user_repo.find_user_by_external_identifier(external_identifier)

    def _create_or_update_user_roles(self, user: User, new_roles: List[Role]):
        user.roles = []

        for role in new_roles:
            existing_role = self.role_repo.find_role(role.name, role.resource.name)
            if not existing_role:
                resource = self.resource_repo.find_resource_by_name(role.resource.name)
                if not resource:
                    raise ResourceNotFound(f"Resource {role.resource.name} does not exist")

                existing_role = Role(
                    name=role.name,
                    resource=resource
                )

            existing_role.operations = role.operations
            user.roles.append(existing_role)

    def create_or_update_user(self, external_identifier: str, user: User) -> User:
        try:
            existing_user = self.find_user_from_external_identifier(external_identifier)
            if not existing_user:
                existing_user = User()

            existing_user.update_single_dimensional_fields(user, external_identifier)
            self._create_or_update_user_roles(existing_user, user.roles)
            user = self.user_repo.create_or_update_user(existing_user)
        except Exception as e:
            raise e

        return user

    def create_user(self, external_identifier: str, user: User) -> User:
        new_user = User()
        new_user.update_single_dimensional_fields(user, external_identifier)
        self._create_or_update_user_roles(new_user, user.roles)

        return self.user_repo.create_user(new_user)

    def get_all_existing_roles(
            self, limit: int,
            role_name: Optional[str] = None,
            resource_name: Optional[str] = None
    ) -> List[Role]:
        return self.role_repo.get_all_roles(limit, role_name, resource_name)

    def create_or_update_role(self, role: Role):
        return self.role_repo.create_or_update_role(role)
