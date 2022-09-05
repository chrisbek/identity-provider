from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.src.business_logic.exception.exceptions import ResourceAlreadyExists
from app.src.business_logic.model.resource import Resource
from app.src.business_logic.services.resource_repository_interface import ResourceRepositoryInterface


class ResourceRepository(ResourceRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def create_resource(self, resource: Resource) -> Resource:
        try:
            self.session.add(resource)
            self.session.flush()
            self.session.commit()
        except IntegrityError as e:
            raise ResourceAlreadyExists(f"Resource {resource.name} already exists")

        return resource

    def find_resource_by_name(self, name: str) -> Optional[Resource]:
        return self.session.query(Resource).filter(Resource.name == name) \
            .first()
