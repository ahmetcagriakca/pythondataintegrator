from typing import Type, TypeVar

from injector import inject

from IocManager import IocManager
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from models.configs.DatabaseConfig import DatabaseConfig

T = TypeVar('T')


class RepositoryProvider(IScoped):
    @inject
    def __init__(self,
                 database_config: DatabaseConfig = None,
                 database_session_manager: DatabaseSessionManager = None
                 ):
        self.database_config = database_config
        self.database_session_manager = database_session_manager

    def create(self) -> DatabaseSessionManager:
        if self.database_session_manager is None:
            if self.database_config is not None:
                self.database_session_manager = DatabaseSessionManager(database_config=self.database_config)
            else:
                self.database_config = IocManager.config_manager.get(DatabaseConfig)
                self.database_session_manager = DatabaseSessionManager(database_config=self.database_config)
            return self.database_session_manager
        else:
            return self.database_session_manager

    def get(self, repository_type: Type[T]) -> Repository[T]:
        database_session_manager = self.create()
        repository = Repository[repository_type](database_session_manager)
        return repository

    def close(self):
        if self.database_session_manager is not None:
            self.database_session_manager.close()
            self.database_session_manager = None
