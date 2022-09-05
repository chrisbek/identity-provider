from typing import List
from fastapi import APIRouter
from app.src.business_logic.exception.exceptions import ResourceNotFound, get_exception_responses_for_codes
from app.src.io.dto.role_dto import SimpleRoleDTO
from app.src.config.dependency_injection import Container

router = APIRouter()
logger = Container.logger()
identity_service = Container.identity_service()
user_serializer = Container.user_serializer()


@router.get("/user/{external_identifier}/roles",
            responses=get_exception_responses_for_codes([404]),
            response_model=List[SimpleRoleDTO])
async def get_role(external_identifier: str) -> List[SimpleRoleDTO]:
    user = identity_service.find_user_from_external_identifier(external_identifier)
    if not user:
        raise ResourceNotFound(f'User {external_identifier} not found')

    user_dto = user_serializer.get_user_dto_from_user(user)
    return user_dto.roles


@router.put("/roles", responses=get_exception_responses_for_codes([409, 404]), response_model=SimpleRoleDTO)
async def put_role(role_dto: SimpleRoleDTO) -> SimpleRoleDTO:
    role = user_serializer.get_role_from_simple_role_dto(role_dto)
    updated_role = identity_service.create_or_update_role(role)

    return user_serializer.get_simple_role_dto_from_role(updated_role)


@router.get("/roles", responses=get_exception_responses_for_codes([]), response_model=List[SimpleRoleDTO])
async def get_all_roles(limit: int = 10) -> List[SimpleRoleDTO]:
    roles = identity_service.get_all_existing_roles(limit)

    return user_serializer.get_list_of_role_dto_from_roles(roles)


@router.get("/roles/{role_name}",
            responses=get_exception_responses_for_codes([404]),
            response_model=List[SimpleRoleDTO])
async def get_all_roles(role_name: str, limit: int = 10) -> List[SimpleRoleDTO]:
    roles = identity_service.get_all_existing_roles(limit, role_name)

    return user_serializer.get_list_of_role_dto_from_roles(roles)


@router.get("/roles/{role_name}/resource/{resource_name}",
            responses=get_exception_responses_for_codes([404]),
            response_model=List[SimpleRoleDTO])
async def get_roles(role_name: str, resource_name: str, limit: int = 10) -> List[SimpleRoleDTO]:
    roles = identity_service.get_all_existing_roles(limit, role_name, resource_name)

    return user_serializer.get_list_of_role_dto_from_roles(roles)
