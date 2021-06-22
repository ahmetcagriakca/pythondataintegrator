from functools import lru_cache

from injector import inject

from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from models.dao.common.ConfigParameter import ConfigParameter


class ConfigService(IScoped):
    @inject
    def __init__(self, database_session_manager: DatabaseSessionManager):
        self.database_session_manager = database_session_manager
        self.config_repository: Repository[ConfigParameter] = Repository[ConfigParameter](
            database_session_manager)

    @lru_cache()
    def get_config_by_name(self, name):
        parameter = self.config_repository.first(Name=name)
        if parameter is not None:
            return parameter.Value
        else:
            return None
