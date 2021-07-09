from functools import lru_cache

from injector import inject

from infrastructor.data.RepositoryProvider import RepositoryProvider
from infrastructor.dependency.scopes import IScoped
from models.dao.common.ConfigParameter import ConfigParameter


class ConfigService(IScoped):
    @inject
    def __init__(self, repository_provider: RepositoryProvider):
        self.config_repository = repository_provider.get(ConfigParameter)

    @lru_cache()
    def get_config_by_name(self, name):
        parameter = self.config_repository.first(Name=name)
        if parameter is not None:
            return parameter.Value
        else:
            return None
