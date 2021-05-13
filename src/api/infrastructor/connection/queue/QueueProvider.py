from injector import inject

from domain.connection.services.ConnectionSecretService import ConnectionSecretService
from domain.connection.services.ConnectionServerService import ConnectionServerService
from infrastructor.connection.queue.connectors.KafkaConnector import KafkaConnector
from infrastructor.connection.queue.QueueContext import QueueContext
from infrastructor.connection.queue.connectors.QueueConnector import QueueConnector
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
from models.configs.ApiConfig import ApiConfig
from models.dao.connection import Connection
from models.enums import ConnectionTypes, ConnectorTypes


class QueueProvider(IScoped):
    @inject
    def __init__(self,
                 sql_logger: SqlLogger,
                 connection_secret_service: ConnectionSecretService,
                 connection_server_service: ConnectionServerService,
                 api_config: ApiConfig
                 ):
        self.connection_server_service = connection_server_service
        self.api_config = api_config
        self.connection_secret_service = connection_secret_service
        self.sql_logger = sql_logger

    def get_context(self, connection: Connection) -> QueueContext:
        """
        Creating Connection
        """
        if connection.ConnectionType.Name == ConnectionTypes.Queue.name:
            connection_basic_authentication = self.connection_secret_service.get_connection_basic_authentication(
                connection_id=connection.Id)
            connection_servers = self.connection_server_service.get_all_by_connection_id(
                connection_id=connection.Id)
            connector: QueueConnector = None
            if connection.Queue.ConnectorType.Name == ConnectorTypes.Kafka.name:
                servers = []
                for connection_server in connection_servers:
                    server = f"{connection_server.Host}:{connection_server.Port}"
                    servers.append(server)
                auth = None
                if ((connection.Queue.Protocol is not None and connection.Queue.Protocol != '') and (
                        connection.Queue.Mechanism is not None and connection.Queue.Mechanism != '') and (
                        connection_basic_authentication.User is not None and connection_basic_authentication.User != '') and (
                        connection_basic_authentication.Password is not None and connection_basic_authentication.Password != '')):
                    auth = {
                        'security_protocol': connection.Queue.Protocol,
                        'sasl_mechanism': connection.Queue.Mechanism,
                        'sasl_plain_username': connection_basic_authentication.User,
                        'sasl_plain_password': connection_basic_authentication.Password
                    }
                connector = KafkaConnector(servers=servers, auth=auth)
            if connector is not None:
                queue_context: QueueContext = QueueContext(connector=connector)
                return queue_context
            else:
                raise Exception(f"{connection.Queue.ConnectorType.Name} connector type not supported")

        else:
            raise Exception(f"{connection.ConnectionType.Name} connection type not supported")
