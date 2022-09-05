from sqlalchemy import Column, Enum, Integer
from app.src.business_logic.model.operation_type import OperationType
from app.src.config.database import Base


class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(Enum(OperationType), unique=True, nullable=False)

