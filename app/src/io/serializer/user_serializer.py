from typing import Optional, Iterator, List
from app.src.business_logic.exception.exceptions import ResourceNotFound
from app.src.business_logic.model.operation_type import OperationType
from app.src.business_logic.services.logger_service import Logger
from app.src.business_logic.services.operation_repository_interface import OperationRepositoryInterface
from app.src.business_logic.services.resource_repository_interface import ResourceRepositoryInterface
from app.src.business_logic.services.role_repository_interface import RoleRepositoryInterface
from app.src.io.dto.user_dto import UserInDTO, UserOutDTO
from app.src.io.dto.role_dto import SimpleRoleDTO
from app.src.business_logic.model.user import User
from app.src.business_logic.model.role import Role
from app.src.business_logic.model.resource import Resource


class UserSerializer:
    def __init__(
            self,
            logger: Logger,
            role_repo: RoleRepositoryInterface,
            resource_repo: ResourceRepositoryInterface,
            operation_repo: OperationRepositoryInterface,
    ):
        self.role_repo = role_repo
        self.resource_repo = resource_repo
        self.operation_repo = operation_repo
        self.logger = logger

    def _add_operation_types_to_role(self, role: Role, operations: Iterator[OperationType]):
        for operation in operations:
            existing_operations = list(filter(lambda o: o.name == operation, role.operations))
            if len(existing_operations) > 0:
                continue
            else:
                operation_model = self.operation_repo.find_operation_by_name(operation)
                if not operation_model:
                    raise ResourceNotFound(f"Operation {operation} not found")

                role.operations.append(operation_model)

    def get_role_from_simple_role_dto(self, simple_role_dto: SimpleRoleDTO) -> Role:
        role = Role(name=self._get_role_name_from_simple_role_dto(simple_role_dto))
        role.resource = Resource(name=self._get_resource_name_from_simple_role_dto(simple_role_dto))
        self._add_operation_types_to_role(role, self._get_operation_types_from_simple_role_dto(simple_role_dto))

        return role

    def _get_operation_types_from_simple_role_dto(self, simple_role_dto: SimpleRoleDTO) -> Iterator[OperationType]:
        for operation in simple_role_dto.role.split(":")[2].split("."):
            yield OperationType(operation)

    def _get_resource_name_from_simple_role_dto(self, simple_role_dto: SimpleRoleDTO) -> str:
        return simple_role_dto.role.split(":")[1]

    def _get_role_name_from_simple_role_dto(self, simple_role_dto: SimpleRoleDTO) -> str:
        return simple_role_dto.role.split(":")[0]

    def _get_corresponding_role_from_user(self, user: User, simple_role_dto: SimpleRoleDTO) -> Optional[Role]:
        """
        Returns the corresponding Role of the simple_role_dto, if the latter belongs to the user.
        Returns null otherwise.
        """
        existing_rules = list(
            filter(
                lambda r:
                r.name == self._get_role_name_from_simple_role_dto(simple_role_dto)
                and r.resource.name == self._get_resource_name_from_simple_role_dto(simple_role_dto),
                user.roles
            )
        )
        if len(existing_rules) == 1:
            return existing_rules[0]
        elif len(existing_rules) == 0:
            return None
        else:
            raise Exception('add message here')

    def _add_simple_role_dto_to_user(self, user: User, simple_role_dto: SimpleRoleDTO):
        existing_role = self._get_corresponding_role_from_user(user, simple_role_dto)
        if existing_role:
            self._add_operation_types_to_role(
                existing_role,
                self._get_operation_types_from_simple_role_dto(simple_role_dto)
            )
        else:
            user.roles.append(
                self.get_role_from_simple_role_dto(simple_role_dto)
            )

    def get_user_from_user_dto(self, user_dto: UserInDTO) -> User:
        user = User()
        user.first_name = user_dto.first_name
        user.email = user_dto.email_address
        for simple_role_dto in user_dto.roles:
            self._add_simple_role_dto_to_user(user, simple_role_dto)

        return user

    def get_simple_role_dto_from_role(self, role: Role) -> SimpleRoleDTO:
        role_identifier_string = role.name + ":" + role.resource.name

        if len(role.operations) > 0:
            role_identifier_string += ":"
            for operation in role.operations:
                role_identifier_string += operation.name + "."
            role_identifier_string = role_identifier_string[:-1]

        return SimpleRoleDTO(role=role_identifier_string)

    def get_user_dto_from_user(self, user: User) -> UserOutDTO:
        user_dto = UserOutDTO(
            external_identifier=user.external_identifier,
            internal_identifier=user.internal_identifier,
            created_at=user.created_at,
            modified_at=user.modified_at,
            email_address=user.email,
            first_name=user.first_name
        )
        for role in user.roles:
            user_dto.roles.append(self.get_simple_role_dto_from_role(role))

        return user_dto

    def get_list_of_role_dto_from_roles(self, roles: List[Role]) -> List[SimpleRoleDTO]:
        role_dtos = []
        for role in roles:
            role_dtos.append(self.get_simple_role_dto_from_role(role))

        return role_dtos
