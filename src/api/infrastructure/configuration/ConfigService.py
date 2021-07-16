from functools import lru_cache

from injector import inject

from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.data.Repository import Repository
from infrastructure.dependency.scopes import IScoped
from models.dao.common.ConfigParameter import ConfigParameter


class ConfigService(IScoped):
    @inject
    def __init__(self, repository_provider: RepositoryProvider):
        self.repository_provider = repository_provider
        self.config_reposiotry = repository_provider.get(ConfigParameter)

    @lru_cache()
    def get_config_by_name(self, name):
        parameter = self.config_reposiotry.first(Name=name)
        if parameter is not None:
            return parameter.Value
        else:
            return None
