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
                 api_config: ApiConfig,
                 console_logger: ConsoleLogger):
        self.api_config = api_config
        self.engine = None
        connection_string = Utils.get_connection_string(database_config=database_config)
        # if database_config.connection_string is not None and database_config.connection_string != '':
        self.engine = create_engine(connection_string, poolclass=pool.NullPool)
        # else:
        #     console_logger.error("Connection string is empty")
        # use session_factory() to get a new Session
        self._SessionFactory = None
        if self.engine is not None:
            self._SessionFactory = sessionmaker(bind=self.engine)
        self.session: Session = None
        self.session: Session = self.session_factory()

    def __del__(self):
        close = getattr(self, "close", None)
        if callable(close):
            self.close()

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

    def close(self):
        if self.session is not None:
            self.session.close()
        if self.engine is not None:
            self.engine.dispose()
            self.engine = None
