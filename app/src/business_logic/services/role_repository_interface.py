from typing import Optional, List
from app.src.business_logic.model.role import Role


class RoleRepositoryInterface:
    def create_role(self, resource: Role) -> Role:
        pass

    def create_or_update_role(self, role: Role) -> Role:
        pass

    def find_role(self, name: str, resource_name: str) -> Optional[Role]:
        pass

    def get_all_roles(
            self, limit: int,
            role_name: Optional[str] = None,
            resource_name: Optional[str] = None
    ) -> List[Role]:
        pass
