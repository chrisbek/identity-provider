from typing import Optional, List
from app.src.business_logic.model.operation import Operation
from app.src.business_logic.model.operation_type import OperationType


class OperationRepositoryInterface:
    def create_operation(self, operation: Operation) -> Operation:
        pass

    def find_operation_by_name(self, name: str) -> Optional[Operation]:
        pass

    def add_required_operation_types(self, operation_types: List[str]):
        pass
