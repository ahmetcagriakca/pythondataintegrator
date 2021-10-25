from injector import inject

from pdip.cryptography import CryptoService
from pdip.data import RepositoryProvider
from pdip.dependency import IScoped
from pdip.exceptions import OperationalException
from models.dao.secret import SecretSource, SecretSourceBasicAuthentication
from models.dto.ConnectionBasicAuthentication import ConnectionBasicAuthentication


class SecretSourceBasicAuthenticationService(IScoped):

    @inject
    def __init__(self,
                 crypto_service: CryptoService,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        self.secret_source_basic_authentication_repository = repository_provider.get(SecretSourceBasicAuthentication)
        self.crypto_service = crypto_service

    def get_by_secret_source(self, secret_source: SecretSource) -> ConnectionBasicAuthentication:
        secret_source_basic_authentication = self.secret_source_basic_authentication_repository.first(
            IsDeleted=0, SecretSource=secret_source)
        connection_basic_authentication = ConnectionBasicAuthentication(
            User=self.crypto_service.decrypt_code(secret_source_basic_authentication.User.encode()).decode('utf-8'),
            Password=self.crypto_service.decrypt_code(secret_source_basic_authentication.Password.encode()).decode('utf-8'))

        return connection_basic_authentication

    def create(self, secret_source: SecretSource, user: str, password: str) -> SecretSourceBasicAuthentication:
        """
        Create SecretSourceBasicAuthentication
        """

        secret_source_basic_authentication = SecretSourceBasicAuthentication(
            User=self.crypto_service.encrypt_code(user.encode()).decode(),
            Password=self.crypto_service.encrypt_code(password.encode()).decode(),
            SecretSource=secret_source)
        self.secret_source_basic_authentication_repository.insert(secret_source_basic_authentication)
        return secret_source

    def update(self, secret_source: SecretSource, user: str, password: str) -> SecretSourceBasicAuthentication:
        """
        Update SecretSourceBasicAuthentication
        """
        secret_source_basic_authentication = self.secret_source_basic_authentication_repository.first(
            IsDeleted=0, SecretSource=secret_source)
        if secret_source_basic_authentication is None:
            raise OperationalException("Secret Source Basic Authentication Not Found")
        secret_source_basic_authentication.User = self.crypto_service.encrypt_code(user.encode()).decode()
        secret_source_basic_authentication.Password = self.crypto_service.encrypt_code(password.encode()).decode()

        return secret_source

    def delete(self, id: int):
        """
        Delete SecretSourceBasicAuthentication
        """
        secret_source_basic_authentication = self.secret_source_basic_authentication_repository.first(Id=id,
                                                                                                      IsDeleted=0)
        if secret_source_basic_authentication is None:
            raise OperationalException("Secret Source Basic Authentication Not Found")

        self.secret_source_basic_authentication_repository.delete_by_id(secret_source_basic_authentication.Id)
