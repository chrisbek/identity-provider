from sqlalchemy import Column, Integer, String, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from app.src.config.database import Base

role_operation_association = \
    Table('role_operation_association', Base.metadata,
          Column('role_id', ForeignKey('roles.id')),
          Column('operation_id', ForeignKey('operations.id'))
          )


class Role(Base):
    __tablename__ = "roles"
    __table_args__ = (
        UniqueConstraint('name', 'resource_id', name='_name_resource_unique_per_role'),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    resource_id = Column(Integer, ForeignKey('resources.id'))

    resource = relationship("Resource", backref=backref("role", uselist=False), lazy='subquery')
    operations = relationship("Operation", secondary=role_operation_association, uselist=True)
