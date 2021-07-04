from injector import inject

from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.data.RepositoryProvider import RepositoryProvider
from infrastructor.dependency.scopes import IScoped
from models.dao.secret import SecretType


class SecretTypeService(IScoped):

    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        self.secret_type_repository = repository_provider.get(SecretType)

    def get_by_name(self, name) -> SecretType:
        """
        Get secret type
        """
        entity = self.secret_type_repository.first(IsDeleted=0, Name=name)
        return entity
