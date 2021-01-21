from injector import inject
from sqlalchemy import create_engine, pool
from sqlalchemy.orm import sessionmaker, Session

from infrastructor.IocManager import IocManager
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.ConsoleLogger import ConsoleLogger
from infrastructor.utils.Utils import Utils
from models.configs.ApiConfig import ApiConfig
from models.configs.DatabaseConfig import DatabaseConfig


class DatabaseSessionManager(IScoped):
    @inject
    def __init__(self,
                 database_config: DatabaseConfig,
                 api_config: ApiConfig):
        self.api_config = api_config
        self.database_config = database_config
        self.engine = None
        self._SessionFactory = None
        self.session: Session = None
        self.connect()

    def __del__(self):
        close = getattr(self, "close", None)
        if callable(close):
            self.close()

    def connect(self):
        self.close()
        connection_string = Utils.get_connection_string(database_config=self.database_config)
        self.engine = create_engine(connection_string, poolclass=pool.NullPool)
        if self.engine is not None:
            self._SessionFactory = sessionmaker(bind=self.engine)
        self.session: Session = self.session_factory()

    def close(self):
        if self.session is not None:
            self.session.close()
        if self.engine is not None:
            self.engine.dispose()
            self.engine = None

    def session_factory(self):
        if self._SessionFactory is not None:
            self.session = self._SessionFactory()
        return self.session

    def commit(self):
        if self.session is not None:
            self.session.commit()

    def rollback(self):
        if self.session is not None:
            self.session.flush()
            self.session.rollback()
            self.session.close()
            self.session: Session = self.session_factory()
