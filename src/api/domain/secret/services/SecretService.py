from injector import inject

from domain.secret.services.SecretSourceService import SecretSourceService
from domain.secret.services.SecretTypeService import SecretTypeService
from pdip.data import RepositoryProvider
from pdip.dependency import IScoped
from pdip.exceptions import OperationalException
from models.dao.secret import Secret
from models.dto.ConnectionBasicAuthentication import ConnectionBasicAuthentication
from models.enums import SecretTypes


class SecretService(IScoped):

    @inject
    def __init__(self,
                 secret_type_service: SecretTypeService,
                 secret_source_service: SecretSourceService,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        self.secret_repository = repository_provider.get(Secret)
        self.secret_type_service = secret_type_service
        self.secret_source_service = secret_source_service

    def create_secret(self, name: str, type: str) -> Secret:
        secret_type = self.secret_type_service.get_by_name(name=type)
        secret = Secret(Name=name, SecretType=secret_type)
        return secret

    def get_basic_authentication(self, id: str) -> ConnectionBasicAuthentication:
        """
        Create File connection
        """
        secret = self.secret_repository.first(IsDeleted=0, Id=id)
        connection_basic_authentication = self.secret_source_service.get_basic_authentication(secret=secret)
        return connection_basic_authentication

    def create_basic_authentication(self, name: str, user: str, password: str) -> Secret:
        """
        Create File connection
        """
        secret = self.create_secret(name=name, type=SecretTypes.Source.name)
        self.secret_source_service.create_basic_authentication(secret=secret, user=user, password=password)
        return secret

    def update_basic_authentication(self, id: int, user: str, password: str) -> Secret:
        """
        Create File connection
        """
        secret = self.secret_repository.first(IsDeleted=0, Id=id)
        if secret is None:
            raise OperationalException("Secret Not Found")
        else:
            self.secret_source_service.update_basic_authentication(secret=secret, user=user, password=password)
        return secret

    def delete_secret(self, id: int):
        """
        Delete Database connection
        """
        secret = self.secret_repository.first(Id=id, IsDeleted=0)
        if secret is None:
            raise OperationalException("Secret Not Found")

        self.secret_repository.delete_by_id(secret.Id)
        if secret.SecretSources is not None:
            for secret_source in secret.SecretSources:
                self.secret_source_service.delete(id=secret_source.Id)
