from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped

from src.domain.secret import AuthenticationType


class AuthenticationTypeService(IScoped):

    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        self.authentication_type_repository = repository_provider.get(AuthenticationType)

    def get_by_name(self, name) -> AuthenticationType:
        """
        Get secret type
        """
        entity = self.authentication_type_repository.first(IsDeleted=0, Name=name)
        return entity

    def get_by_id(self, id) -> AuthenticationType:
        """
        Get secret type
        """
        entity = self.authentication_type_repository.first(IsDeleted=0, Id=id)
        return entity
