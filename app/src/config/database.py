from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.util.compat import contextmanager
from app.src.business_logic.services.logger_service import Logger

Base = declarative_base()


class Database:
    def __init__(
            self,
            logger: Logger,
            dialect_and_driver: str = "mysql+pymysql",
            username: str = "identity_provider_user",
            password: str = "local_pass",
            host: str = "172.30.0.4",
            port: str = "3306",
            database: str = "identity_provider"
    ) -> None:
        # dialect+driver://username:password@host:port/database
        db_url = f"{dialect_and_driver}://{username}:{password}@{host}:{port}/{database}"

        self.logger = logger
        self.url = db_url
        self._engine = create_engine(self.url, echo=True)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
                expire_on_commit=False,
            ),
        )
        self.session = self._session_factory()

    def create_database(self) -> None:
        """
        This one creates the tables from their metadata. We don't need it, since we use alembic for this purpose.
        """
        Base.metadata.create_all(self._engine)

    # @contextmanager
    # def session(self) -> Callable[..., AbstractContextManager[Session]]:
    #     session: Session = self._session_factory()
    #     try:
    #         yield session
    #     except Exception:
    #         self.logger.logger.exception('Session rollback because of exception')
    #         session.rollback()
    #         raise
    #     finally:
    #         session.close()

    def __getstate__(self):
        """
        We need to pickle an object that has a database connection but that's an unserializable object.
        The solution is to freeze the object out from the serialization process
        (do not serialize the connection parts).
        We use the __getstate__ method for this purpose.
        """
        d = self.__dict__.copy()
        del d['_session_factory']
        del d['_engine']
        return d

    def __setstate__(self, d):
        """
        When reinitializing the connection after the object is deserialized we need to re-create the connection.
        We use the __setstate__ method for this purpose.
        """
        d['_engine'] = create_engine(d['url'], echo=True)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=d['_engine'],
            )
        )
        self.__dict__.update(d)
