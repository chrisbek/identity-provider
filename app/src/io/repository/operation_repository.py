from typing import Optional, List
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from app.src.business_logic.exception.exceptions import ResourceAlreadyExists
from app.src.business_logic.model.operation import Operation
from app.src.business_logic.services.logger_service import Logger
from app.src.business_logic.services.operation_repository_interface import OperationRepositoryInterface


class OperationRepository(OperationRepositoryInterface):
    def __init__(self, logger: Logger, session: Session):
        self.logger = logger
        self.session = session

    def create_operation(self, operation: Operation) -> Operation:
        try:
            self.session.add(operation)
            self.session.flush()
            self.session.commit()
        except IntegrityError as e:
            raise ResourceAlreadyExists(f"Operation {operation.name} already exists")

        return operation

    def find_operation_by_name(self, name: str) -> Optional[Operation]:
        return self.session.query(Operation).filter(Operation.name == name) \
            .first()

    def add_required_operation_types(self, operation_types: List[str]):
        for operation_type in operation_types:
            try:
                self.session.add(Operation(name=operation_type))
                self.session.commit()
            except SQLAlchemyError:  # The actual exception depends on the specific database
                self.session.rollback()
