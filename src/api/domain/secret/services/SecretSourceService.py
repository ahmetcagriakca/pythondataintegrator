from injector import inject

from domain.secret.services.AuthenticationTypeService import AuthenticationTypeService
from domain.secret.services.SecretSourceBasicAuthenticationService import SecretSourceBasicAuthenticationService
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.data.RepositoryProvider import RepositoryProvider
from infrastructor.dependency.scopes import IScoped
from infrastructor.exceptions.OperationalException import OperationalException
from models.dao.secret import Secret, SecretSource
from models.dto.ConnectionBasicAuthentication import ConnectionBasicAuthentication
from models.enums import AuthenticationTypes


class SecretSourceService(IScoped):

    @inject
    def __init__(self,
                 authentication_type_service: AuthenticationTypeService,
                 secret_source_basic_authentication_service: SecretSourceBasicAuthenticationService,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        self.secret_source_repository = repository_provider.get(SecretSource)
        self.secret_source_basic_authentication_service = secret_source_basic_authentication_service
        self.authentication_type_service = authentication_type_service

    def create_secret_source(self, secret: Secret, authentication_type_name):
        authentication_type = self.authentication_type_service.get_by_name(
            name=authentication_type_name)
        secret_source = SecretSource(AuthenticationType=authentication_type, Secret=secret)
        self.secret_source_repository.insert(secret_source)
        return secret_source

    def get_basic_authentication(self, secret: Secret) -> ConnectionBasicAuthentication:
        """
        Create File connection
        """
        secret_source = self.secret_source_repository.first(IsDeleted=0, Secret=secret)
        connection_basic_authentication=self.secret_source_basic_authentication_service.get_by_secret_source(secret_source=secret_source)
        return connection_basic_authentication

    def create_basic_authentication(self, secret: Secret, user: str, password: str) -> SecretSource:
        """
        Create File connection
        """
        secret_source = self.create_secret_source(authentication_type_name=AuthenticationTypes.BasicAuthentication.name,
                                                  secret=secret)
        self.secret_source_basic_authentication_service.create(secret_source=secret_source, user=user,
                                                               password=password)
        return secret_source

    def update_basic_authentication(self, secret: Secret, user: str, password: str) -> SecretSource:
        """
        Create File connection
        """
        secret_source = self.secret_source_repository.first(IsDeleted=0, Secret=secret)
        if secret_source is None:
            raise OperationalException("Secret Source Not Found")
        self.secret_source_basic_authentication_service.update(secret_source=secret_source, user=user,
                                                               password=password)
        return secret_source

    def delete(self, id: int):
        """
        Delete Secret Source
        """
        secret_source = self.secret_source_repository.first(Id=id, IsDeleted=0)
        if secret_source is None:
            raise OperationalException("Secret Source Not Found")

        self.secret_source_repository.delete_by_id(secret_source.Id)
        if secret_source.SecretSourceBasicAuthentications is not None:
            for secret_source_basic_authentication in secret_source.SecretSourceBasicAuthentications:
                self.secret_source_basic_authentication_service.delete(id=secret_source_basic_authentication.Id)
