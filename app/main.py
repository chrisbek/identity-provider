from fastapi import FastAPI
from app.src.config.debug import start_debug_client
from app.src.config.init import on_startup
from app.src.config.middleware import catch_exceptions_middleware
from app.src.io.controllers import user_controller
from app.src.io.controllers import role_controller

debug = False
if debug:
    start_debug_client()

app = FastAPI(
    on_startup=on_startup(),
    title="identity-provider"
)
app.middleware('http')(catch_exceptions_middleware)
app.include_router(user_controller.router)
app.include_router(role_controller.router)
