import sys
from app.src.config.dependency_injection import Container


def on_startup():
    container = Container()
    container.wire(modules=[sys.modules[__name__]])
    logger = container.logger()
    logger.info("Ready to handle connections:")
    # db = container.db()
    # db.create_database() - We don't need it, since we use alembic for this purpose.
