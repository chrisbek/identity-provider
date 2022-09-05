from sqlalchemy import Column, String, DateTime, func, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.src.config.database import Base
import uuid

user_role_association = \
    Table('user_role_association', Base.metadata,
          Column('user_id', ForeignKey('users.id')),
          Column('role_id', ForeignKey('roles.id')),
          )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    external_identifier = Column(String(200), unique=True, nullable=False)
    internal_identifier = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    email = Column(String(50), unique=True)
    first_name = Column(String(100))

    roles = relationship("Role", secondary=user_role_association, uselist=True, lazy='subquery')

    def update_single_dimensional_fields(self, user: 'User', external_identifier: str):
        self.internal_identifier = User._get_new_internal_identifier()
        self.external_identifier = external_identifier
        self.email = user.email
        self.first_name = user.first_name

    @staticmethod
    def _get_new_internal_identifier() -> str:
        return uuid.uuid4().hex
