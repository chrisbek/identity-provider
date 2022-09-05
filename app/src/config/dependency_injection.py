from dependency_injector import containers, providers
from app.src.business_logic.model.operation_type import OperationType
from app.src.business_logic.services.identity_service import IdentityService
from app.src.business_logic.services.logger_service import Logger
from app.src.config.database import Database
from app.src.io.repository.operation_repository import OperationRepository
from app.src.io.repository.resource_repository import ResourceRepository
from app.src.io.repository.role_repository import RoleRepository
from app.src.io.repository.user_repository import UserRepository
from app.src.io.serializer.user_serializer import UserSerializer


def _initialize_operations(operation_repo: OperationRepository):
    operation_repo.add_required_operation_types(
        [operation_type for operation_type in OperationType]
    )


class Container(containers.DeclarativeContainer):
    logger = providers.Singleton(Logger)

    db = providers.Singleton(
        Database,
        logger=logger
    )
    db_session = db.provided.session

    user_repository = providers.Singleton(
        UserRepository,
        session=db_session,
        logger=logger
    )

    resource_repo = providers.Singleton(
        ResourceRepository,
        session=db_session
    )

    operation_repo = providers.Singleton(
        OperationRepository,
        logger=logger,
        session=db_session
    )
    _initialize_operations(operation_repo.provided())

    role_repo = providers.Singleton(
        RoleRepository,
        session=db_session,
        logger=logger
    )

    identity_service = providers.Singleton(
        IdentityService,
        logger=logger,
        user_repo=user_repository,
        resource_repo=resource_repo,
        operation_repo=operation_repo,
        role_repo=role_repo
    )

    user_serializer = providers.Singleton(
        UserSerializer,
        logger=logger,
        role_repo=role_repo,
        resource_repo=resource_repo,
        operation_repo=operation_repo,
    )
