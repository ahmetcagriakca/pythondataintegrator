from injector import inject
from domain.secret.services.SecretService import SecretService
from infrastructor.data.RepositoryProvider import RepositoryProvider
from infrastructor.dependency.scopes import IScoped
from infrastructor.exceptions.OperationalException import OperationalException
from models.dao.connection import ConnectionSecret
from models.dao.connection.Connection import Connection
from models.dto.ConnectionBasicAuthentication import ConnectionBasicAuthentication


class ConnectionSecretService(IScoped):

    @inject
    def __init__(self,
                 secret_service: SecretService,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        self.connection_secret_repository = repository_provider.get(ConnectionSecret)
        self.secret_service = secret_service

    def get_connection_basic_authentication(self, connection_id: int) -> ConnectionBasicAuthentication:
        connection_secret = self.connection_secret_repository.first(IsDeleted=0, ConnectionId=connection_id)
        connection_basic_authentication = self.secret_service.get_basic_authentication(id=connection_secret.SecretId)
        return connection_basic_authentication

    def create(self, connection: Connection, user: str, password: str) -> ConnectionSecret:
        """
        Create ConnectionSecret
        """
        secret = self.secret_service.create_basic_authentication(name=connection.Name, user=user, password=password)
        connection_secret = ConnectionSecret(Connection=connection, Secret=secret)
        self.connection_secret_repository.insert(connection_secret)
        return connection_secret

    def update(self, connection: Connection, user: str, password: str) -> ConnectionSecret:
        """
        Update ConnectionSecret
        """
        connection_secret = self.connection_secret_repository.first(IsDeleted=0, Connection=connection)
        if connection_secret is None:
            raise OperationalException("Connection Secret Not Found")
        self.secret_service.update_basic_authentication(id=connection_secret.SecretId, user=user, password=password)

        return connection_secret

    def delete(self, id: int):
        """
        Delete ConnectionSecret
        """

        connection_secret = self.connection_secret_repository.first(IsDeleted=0, Id=id)
        if connection_secret is None:
            raise OperationalException("Connection Secret Not Found")
        self.connection_secret_repository.delete_by_id(id)
        self.secret_service.delete_secret(connection_secret.SecretId)
