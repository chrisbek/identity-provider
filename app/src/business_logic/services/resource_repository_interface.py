from typing import Optional
from app.src.business_logic.model.resource import Resource


class ResourceRepositoryInterface:
    def create_resource(self, resource: Resource) -> Resource:
        pass

    def find_resource_by_name(self, name: str) -> Optional[Resource]:
        pass
