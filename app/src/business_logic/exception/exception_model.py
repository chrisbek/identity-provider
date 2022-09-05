from pydantic import BaseModel


class BusinessExceptionModel(BaseModel):
    error: str
    code: int


class ServerExceptionModel(BaseModel):
    error: str
