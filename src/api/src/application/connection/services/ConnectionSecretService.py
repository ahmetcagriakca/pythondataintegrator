from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped
from pdip.exceptions import OperationalException

from src.application.secret.services.SecretService import SecretService
from src.domain.connection import ConnectionSecret
from src.domain.connection.Connection import Connection
from src.domain.dto.ConnectionBasicAuthentication import ConnectionBasicAuthentication


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

    def create_basic_authentication(self, connection: Connection, user: str, password: str) -> ConnectionSecret:
        """
        Create ConnectionSecret
        """
        if user is None or user == '':
            raise OperationalException("User cannot be null")
        if password is None or password == '':
            raise OperationalException("Password cannot be null")
        secret = self.secret_service.create_basic_authentication(name=connection.Name, user=user, password=password)
        connection_secret = ConnectionSecret(Connection=connection, Secret=secret)
        self.connection_secret_repository.insert(connection_secret)
        return connection_secret

    def update_basic_authentication(self, connection: Connection, user: str, password: str) -> ConnectionSecret:
        """
        Update ConnectionSecret
        """
        if user is None or user == '':
            raise OperationalException("User cannot be null")
        if password is None or password == '':
            raise OperationalException("Password cannot be null")
        connection_secret = self.connection_secret_repository.first(IsDeleted=0, Connection=connection)
        if connection_secret is None:
            raise OperationalException("Connection Secret Not Found")
        self.secret_service.update_basic_authentication(id=connection_secret.SecretId, user=user, password=password)

        return connection_secret

    def create_kerberos_authentication(self, connection: Connection, principal: str, password: str, krb_realm: str,
                                       krb_fqdn: str, krb_service_name: str) -> ConnectionSecret:
        """
        Create ConnectionSecret
        """
        if principal is None or principal == '':
            raise OperationalException("Principal cannot be null")
        if password is None or password == '':
            raise OperationalException("Password cannot be null")
        secret = self.secret_service.create_kerberos_authentication(
            name=connection.Name,
            principal=principal,
            password=password,
            krb_realm=krb_realm,
            krb_fqdn=krb_fqdn,
            krb_service_name=krb_service_name
        )
        connection_secret = ConnectionSecret(Connection=connection, Secret=secret)
        self.connection_secret_repository.insert(connection_secret)
        return connection_secret

    def update_kerberos_authentication(self, connection: Connection, principal: str, password: str, krb_realm: str,
                                       krb_fqdn: str, krb_service_name: str) -> ConnectionSecret:
        """
        Update ConnectionSecret
        """
        if principal is None or principal == '':
            raise OperationalException("Principal cannot be null")
        if password is None or password == '':
            raise OperationalException("Password cannot be null")
        connection_secret = self.connection_secret_repository.first(IsDeleted=0, Connection=connection)
        if connection_secret is None:
            raise OperationalException("Connection Secret Not Found")
        self.secret_service.update_kerberos_authentication(
            id=connection_secret.SecretId,
            principal=principal,
            password=password,
            krb_realm=krb_realm,
            krb_fqdn=krb_fqdn,
            krb_service_name=krb_service_name
        )

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
