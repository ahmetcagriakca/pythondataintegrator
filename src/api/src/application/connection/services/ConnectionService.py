from typing import List

from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped
from pdip.exceptions import OperationalException
from pdip.integrator.connection.domain.authentication.type import AuthenticationTypes
from pdip.integrator.connection.domain.enums import ConnectionTypes
from pdip.logging.loggers.sql import SqlLogger

from src.application.connection.CreateConnectionBigData.CreateConnectionBigDataRequest import \
    CreateConnectionBigDataRequest
from src.application.connection.CreateConnectionFile.CreateConnectionFileRequest import CreateConnectionFileRequest
from src.application.connection.CreateConnectionQueue.CreateConnectionQueueRequest import CreateConnectionQueueRequest
from src.application.connection.CreateConnectionSql.CreateConnectionSqlRequest import \
    CreateConnectionSqlRequest
from src.application.connection.CreateConnectionWebService.CreateConnectionWebServiceRequest import \
    CreateConnectionWebServiceRequest
from src.application.connection.services.ConnectionBigDataService import ConnectionBigDataService
from src.application.connection.services.ConnectionFileService import ConnectionFileService
from src.application.connection.services.ConnectionQueueService import ConnectionQueueService
from src.application.connection.services.ConnectionSecretService import ConnectionSecretService
from src.application.connection.services.ConnectionServerService import ConnectionServerService
from src.application.connection.services.ConnectionSqlService import ConnectionSqlService
from src.application.connection.services.ConnectionTypeService import ConnectionTypeService
from src.application.connection.services.ConnectionWebServiceService import ConnectionWebServiceService
from src.domain.connection.Connection import Connection


class ConnectionService(IScoped):

    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 sql_logger: SqlLogger,
                 connection_type_service: ConnectionTypeService,
                 connection_database_service: ConnectionSqlService,
                 connection_big_data_service: ConnectionBigDataService,
                 connection_file_service: ConnectionFileService,
                 connection_queue_service: ConnectionQueueService,
                 connection_web_service_service: ConnectionWebServiceService,
                 connection_secret_service: ConnectionSecretService,
                 connection_server_service: ConnectionServerService
                 ):
        self.connection_web_service_service = connection_web_service_service
        self.connection_big_data_service = connection_big_data_service
        self.repository_provider = repository_provider
        self.connection_queue_service = connection_queue_service
        self.connection_server_service = connection_server_service
        self.connection_secret_service = connection_secret_service
        self.connection_type_service = connection_type_service
        self.sql_logger: SqlLogger = sql_logger
        self.connection_file_service = connection_file_service
        self.connection_database_service = connection_database_service
        self.connection_repository = repository_provider.get(Connection)

    def get_connections(self) -> List[Connection]:
        """
        Data data_integration data preparing
        """
        connections = self.connection_repository.filter_by(IsDeleted=0).all()
        return connections

    def get_by_name(self, name):
        connection = self.connection_repository.first(IsDeleted=0, Name=name)
        return connection

    def check_connection_name(self, name):
        connection = self.get_by_name(name=name)
        return connection is not None

    def create_connection(self, name: str, connection_type_id: str) -> Connection:
        connection_type = self.connection_type_service.get_by_id(id=connection_type_id)
        connection = Connection(Name=name, ConnectionType=connection_type)
        return connection

    def create_connection_database(self, request: CreateConnectionSqlRequest) -> Connection:
        """
        Create File connection
        """
        connection = self.get_by_name(name=request.Name)
        if connection is None:
            connection = self.create_connection(name=request.Name,
                                                connection_type_id=ConnectionTypes.Sql.value)
            self.connection_secret_service.create_basic_authentication(connection=connection, user=request.User,
                                                                       password=request.Password)
            self.connection_server_service.create(connection=connection, host=request.Host, port=request.Port)
            self.connection_database_service.create(connection=connection,
                                                    connector_type_id=request.ConnectorTypeId, sid=request.Sid,
                                                    service_name=request.ServiceName,
                                                    database_name=request.DatabaseName)
            self.connection_repository.insert(connection)
        else:
            self.connection_secret_service.update_basic_authentication(connection=connection, user=request.User,
                                                                       password=request.Password)
            self.connection_server_service.update(connection=connection, host=request.Host, port=request.Port)
            self.connection_database_service.update(connection=connection,
                                                    connector_type_id=request.ConnectorTypeId, sid=request.Sid,
                                                    service_name=request.ServiceName,
                                                    database_name=request.DatabaseName)
        return connection

    def create_connection_big_data(self, request: CreateConnectionBigDataRequest) -> Connection:
        """
        Create File connection
        """
        connection = self.get_by_name(name=request.Name)
        if connection is None:
            connection = self.create_connection(name=request.Name,
                                                connection_type_id=ConnectionTypes.BigData.value)
            if AuthenticationTypes(request.AuthenticationType) == AuthenticationTypes.BasicAuthentication:
                self.connection_secret_service.create_basic_authentication(
                    connection=connection,
                    user=request.User,
                    password=request.Password
                )
            elif AuthenticationTypes(request.AuthenticationType) == AuthenticationTypes.Kerberos:
                self.connection_secret_service.create_kerberos_authentication(
                    connection=connection,
                    principal=request.User,
                    password=request.Password,
                    krb_realm=request.KrbRealm,
                    krb_fqdn=request.KrbFqdn,
                    krb_service_name=request.KrbServiceName
                )
            self.connection_server_service.create(connection=connection, host=request.Host, port=request.Port)
            self.connection_big_data_service.create(
                connection=connection,
                connector_type_id=request.ConnectorTypeId,
                ssl=request.Ssl,
                use_only_sspi=request.UseOnlySspi,
                database_name=request.DatabaseName
            )
            self.connection_repository.insert(connection)
        else:
            if AuthenticationTypes(request.AuthenticationType) == AuthenticationTypes.BasicAuthentication:
                self.connection_secret_service.update_basic_authentication(
                    connection=connection,
                    user=request.User,
                    password=request.Password
                )
            elif AuthenticationTypes(request.AuthenticationType) == AuthenticationTypes.Kerberos:
                self.connection_secret_service.update_kerberos_authentication(
                    connection=connection,
                    principal=request.User,
                    password=request.Password,
                    krb_realm=request.KrbRealm,
                    krb_fqdn=request.KrbFqdn,
                    krb_service_name=request.KrbServiceName
                )
            self.connection_server_service.update(connection=connection, host=request.Host, port=request.Port)
            self.connection_big_data_service.update(connection=connection,
                                                    connector_type_id=request.ConnectorTypeId, ssl=request.Ssl,
                                                    use_only_sspi=request.UseOnlySspi,
                                                    database_name=request.DatabaseName)
        return connection

    def create_connection_file(self, request: CreateConnectionFileRequest) -> Connection:
        """
        Create File connection
        """
        connection = self.get_by_name(name=request.Name)
        if connection is None:
            connection = self.create_connection(name=request.Name,
                                                connection_type_id=ConnectionTypes.File.value)
            self.connection_secret_service.create_basic_authentication(connection=connection, user=request.User,
                                                                       password=request.Password)
            self.connection_server_service.create(connection=connection, host=request.Host, port=request.Port)
            self.connection_file_service.create(connection=connection, connector_type_id=request.ConnectorTypeId)
            self.connection_repository.insert(connection)
        else:
            self.connection_secret_service.update_basic_authentication(connection=connection, user=request.User,
                                                                       password=request.Password)
            self.connection_server_service.update(connection=connection, host=request.Host, port=request.Port)
            self.connection_file_service.update(connection=connection, connector_type_id=request.ConnectorTypeId)

        return connection

    def create_connection_queue(self, request: CreateConnectionQueueRequest) -> Connection:
        """
        Create File connection
        """
        connection = self.get_by_name(name=request.Name)
        if connection is None:
            connection = self.create_connection(name=request.Name,
                                                connection_type_id=ConnectionTypes.Queue.value)
            self.connection_secret_service.create_basic_authentication(connection=connection, user=request.User,
                                                                       password=request.Password)
            for server in request.Servers:
                self.connection_server_service.create(connection=connection, host=server.Host, port=server.Port)
            self.connection_queue_service.create(connection=connection, connector_type_id=request.ConnectorTypeId,
                                                 protocol=request.Protocol, mechanism=request.Mechanism)
            connection = self.connection_repository.first(Id=connection.Id)
        else:
            self.connection_secret_service.update_basic_authentication(connection=connection, user=request.User,
                                                                       password=request.Password)

            for server in request.Servers:
                connection_server = self.connection_server_service.get_by_server_info(connection_id=connection.Id,
                                                                                      host=server.Host,
                                                                                      port=server.Port)
                if connection_server is not None:
                    self.connection_server_service.update(connection=connection, host=server.Host, port=server.Port)
                else:
                    self.connection_server_service.create(connection=connection, host=server.Host, port=server.Port)

            connection_servers = self.connection_server_service.get_all_by_connection_id(connection_id=connection.Id)
            for connection_server in connection_servers:
                check = [server for server in request.Servers if
                         server.Host == connection_server.Host and server.Port == connection_server.Port]
                if check is None or len(check) == 0:
                    self.connection_server_service.delete(id=connection_server.Id)

            self.connection_queue_service.update(connection=connection, connector_type_id=request.ConnectorTypeId,
                                                 protocol=request.Protocol, mechanism=request.Mechanism)
        return connection

    def create_connection_web_service(self, request: CreateConnectionWebServiceRequest) -> Connection:
        """
        Create File connection
        """
        connection = self.get_by_name(name=request.Name)
        if connection is None:
            connection = self.create_connection(name=request.Name,
                                                connection_type_id=ConnectionTypes.WebService.value)
            self.connection_secret_service.create_basic_authentication(connection=connection, user=request.User,
                                                                       password=request.Password)
            for server in request.Servers:
                self.connection_server_service.create(connection=connection, host=server.Host, port=server.Port)
            self.connection_web_service_service.create(connection=connection, connector_type_id=request.ConnectorTypeId,
                                                       ssl=request.Ssl, wsdl=request.Soap.Wsdl)
            connection = self.connection_repository.first(Id=connection.Id)
        else:
            self.connection_secret_service.update_basic_authentication(connection=connection, user=request.User,
                                                                       password=request.Password)

            for server in request.Servers:
                connection_server = self.connection_server_service.get_by_server_info(connection_id=connection.Id,
                                                                                      host=server.Host,
                                                                                      port=server.Port)
                if connection_server is not None:
                    self.connection_server_service.update(connection=connection, host=server.Host, port=server.Port)
                else:
                    self.connection_server_service.create(connection=connection, host=server.Host, port=server.Port)

            connection_servers = self.connection_server_service.get_all_by_connection_id(connection_id=connection.Id)
            for connection_server in connection_servers:
                check = [server for server in request.Servers if
                         server.Host == connection_server.Host and server.Port == connection_server.Port]
                if check is None or len(check) == 0:
                    self.connection_server_service.delete(id=connection_server.Id)

            self.connection_web_service_service.update(connection=connection, connector_type_id=request.ConnectorTypeId,
                                                       ssl=request.Ssl, wsdl=request.Soap.Wsdl)
        return connection

    def delete_connection(self, id: int):
        """
        Delete Database connection
        """
        connection = self.connection_repository.first(Id=id, IsDeleted=0)
        if connection is None:
            raise OperationalException("Connection Not Found")

        self.connection_repository.delete_by_id(connection.Id)
        if connection.Database is not None:
            self.connection_database_service.delete(id=connection.Database.Id)
        if connection.File is not None:
            self.connection_file_service.delete(id=connection.File.Id)
        if connection.BigData is not None:
            self.connection_big_data_service.delete(id=connection.File.Id)

        if connection.ConnectionServers is not None:
            for connection_server in connection.ConnectionServers:
                self.connection_server_service.delete(id=connection_server.Id)
        if connection.ConnectionSecrets is not None:
            for connection_secret in connection.ConnectionSecrets:
                self.connection_secret_service.delete(id=connection_secret.Id)
        message = f'{connection.Name} connection deleted'
        self.sql_logger.info(message)
        return message
