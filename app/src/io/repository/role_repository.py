from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, Query
from app.src.business_logic.exception.exceptions import ResourceAlreadyExists
from app.src.business_logic.model.resource import Resource
from app.src.business_logic.model.role import Role
from app.src.business_logic.services.logger_service import Logger
from app.src.business_logic.services.role_repository_interface import RoleRepositoryInterface


class RoleRepository(RoleRepositoryInterface):
    def __init__(
            self,
            logger: Logger,
            session: Session
    ):
        self.session = session
        self.logger = logger

    def create_role(self, role: Role) -> Role:
        try:
            self.session.add(role)
            self.session.flush()
            self.session.commit()
        except IntegrityError as e:
            raise ResourceAlreadyExists(f"Role {role.name} already exists")

        return role

    def create_or_update_role(self, role: Role) -> Role:
        existing_role = self.find_role(role.name, role.resource.name)
        if existing_role:
            existing_role.operations = role.operations
            self.session.merge(existing_role)
            role = existing_role
        else:
            self.session.merge(role)

        self.session.flush()
        self.session.commit()

        return role

    def find_role(self, name: str, resource_name: str) -> Optional[Role]:
        role = self.session.query(Role) \
            .join(Resource) \
            .filter(Role.resource_id == Resource.id) \
            .filter(Role.name == name) \
            .filter(Resource.name == resource_name) \
            .first()

        return role

    def get_all_roles(
            self, limit: int,
            role_name: Optional[str] = None,
            resource_name: Optional[str] = None
    ) -> List[Role]:
        query: Query = self.session.query(Role)
        if role_name:
            query = query.filter(Role.name == role_name)
        if resource_name:
            query = query \
                .join(Resource) \
                .filter(Resource.name == resource_name)

        return query.limit(limit).all()
