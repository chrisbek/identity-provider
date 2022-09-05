from typing import List

from app.src.business_logic.exception.exception_model import BusinessExceptionModel, ServerExceptionModel


class BusinessException(Exception):
    def __init__(self, error_message: str, code: int = 400, http_status: int = 409):
        super().__init__()
        self.error_message = error_message
        self.http_status = http_status
        self.code = code


class ServerException(Exception):
    def __init__(self, error_message: str, code: int = 500, http_status: int = 500):
        super().__init__()
        self.error_message = error_message
        self.http_status = http_status
        self.code = code


class ResourceAlreadyExists(BusinessException):
    def __init__(self, error_message: str):
        super().__init__(error_message, 401)


class InvalidRoleDefinition(BusinessException):
    def __init__(self, error_message: str):
        super().__init__(error_message, 402)


class ResourceNotFound(BusinessException):
    def __init__(self, error_message: str):
        super().__init__(error_message, 403, 404)


def get_error_message_for_exception(e: Exception) -> str:
    if isinstance(e, ResourceNotFound):
        return "Resource not found"
    if isinstance(e, ResourceAlreadyExists):
        return "Resource already exists"
    if isinstance(e, InvalidRoleDefinition):
        return "Invalid role"

    return str(e)


def get_exception_responses_for_codes(error_codes: List[int]) -> dict:
    responses = {
        409: {"model": BusinessExceptionModel},
        404: {"model": BusinessExceptionModel},
        500: {"model": ServerExceptionModel},
    }

    if 500 not in error_codes:
        error_codes.append(500)
    return {key: responses[key] for key in error_codes}
