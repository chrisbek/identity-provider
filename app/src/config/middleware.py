import json
from starlette.requests import Request
from starlette.responses import Response
from app.src.business_logic.exception.exceptions import get_error_message_for_exception
from app.src.config.dependency_injection import Container


async def catch_exceptions_middleware(request: Request, call_next):
    logger = Container.logger().logger
    session = Container.db_session()
    try:
        return await call_next(request)
    except Exception as e:
        error_message = get_error_message_for_exception(e)
        try:
            http_status = e.__getattribute__('http_status')
        except AttributeError:
            http_status = 500
        try:
            error_code = e.__getattribute__('code')
        except AttributeError:
            error_code = 0

        session.rollback()
        session.close()
        logger.error(f"Error {type(e)}: {error_code}")

        return Response(
            json.dumps({
                'error': error_message,
                'code': error_code
            }),
            status_code=http_status,
            headers={'Content-Type': 'application/json'}
        )
