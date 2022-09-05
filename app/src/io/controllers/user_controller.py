from fastapi import APIRouter
from app.src.business_logic.exception.exceptions import ResourceNotFound, get_exception_responses_for_codes
from app.src.io.dto.user_dto import UserInDTO, UserOutDTO
from app.src.config.dependency_injection import Container

router = APIRouter()
logger = Container.logger()
identity_service = Container.identity_service()
user_serializer = Container.user_serializer()


@router.get("/user/{external_identifier}",
            responses=get_exception_responses_for_codes([404]),
            response_model=UserOutDTO)
async def get_user(external_identifier: str) -> UserOutDTO:
    user = identity_service.find_user_from_external_identifier(external_identifier)
    if not user:
        raise ResourceNotFound(f'User {external_identifier} not found')
    return user_serializer.get_user_dto_from_user(user)


@router.put("/user/{external_identifier}",
            responses=get_exception_responses_for_codes([409, 404]),
            response_model=UserOutDTO)
async def put_user(user_dto: UserInDTO, external_identifier: str) -> UserOutDTO:
    user = user_serializer.get_user_from_user_dto(user_dto)
    updated_user = identity_service.create_or_update_user(external_identifier, user)
    updated_user_dto = user_serializer.get_user_dto_from_user(updated_user)

    return updated_user_dto


@router.post("/user/{external_identifier}",
             responses=get_exception_responses_for_codes([409, 404]),
             response_model=UserOutDTO)
async def post_user(user_dto: UserInDTO, external_identifier: str) -> UserOutDTO:
    user = user_serializer.get_user_from_user_dto(user_dto)
    updated_user = identity_service.create_user(external_identifier, user)
    updated_user_dto = user_serializer.get_user_dto_from_user(updated_user)

    return updated_user_dto
