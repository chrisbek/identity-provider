from pydantic import BaseModel


class SimpleRoleDTO(BaseModel):
    role: str

    class Config:
        orm_mode = True
