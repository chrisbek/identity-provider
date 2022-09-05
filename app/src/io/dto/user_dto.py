from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.src.io.dto.role_dto import SimpleRoleDTO


class BaseUserDTO(BaseModel):
    roles: Optional[List[SimpleRoleDTO]] = []
    email_address: str
    first_name: str

    class Config:
        orm_mode = True

    """
    UserDTO example: {
        email_address: "bekos@gmail.com",
        first_name: "christopher",
        roles: [
            'admin:email:r.w',
            'admin:email:d',
            'admin:post:r.w.d',
            'admin:user:w',
            'admin:user:r',
            'manager:email:r',
            'manager:post:r.w'
        ]
    }
    """


class UserInDTO(BaseUserDTO):
    pass


class UserOutDTO(BaseUserDTO):
    external_identifier: str
    internal_identifier: Optional[str]
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    roles: Optional[List[SimpleRoleDTO]] = []
    email_address: str
    first_name: str
    """
        UserDTO example: {
            external_identifier: "Nie1eeYo6bogoh0eingoonu3",
            internal_identifier: "Eewoo2chah5wi3eishohcieS",
            email_address: "bekos@gmail.com",
            first_name: "christopher",
            roles: [
                'admin:email:r.w.d',
                'admin:post:r.w.d',
                'admin:user:r.w',
                'manager:email:r',
                'manager:post:r.w'
            ]
        }
    """
