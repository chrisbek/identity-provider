from sqlalchemy import Column, Integer, String
from app.src.config.database import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), primary_key=True, index=True)
