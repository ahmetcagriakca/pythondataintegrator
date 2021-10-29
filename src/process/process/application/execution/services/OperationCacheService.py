from typing import List

from injector import inject
from pdip.connection.models.enums import ConnectionTypes
from pdip.cryptography import CryptoService
from pdip.data import RepositoryProvider
from pdip.data.decorators import transactionhandler
from pdip.dependency import IScoped
from pdip.exceptions import OperationalException
from pdip.json import BaseConverter

from process.domain.base.connection import ConnectionBase, ConnectionTypeBase, ConnectionDatabaseBase, \
    ConnectionFileBase, \
    ConnectionQueueBase, ConnectionServerBase, ConnectionSecretBase
from process.domain.base.integration import DataIntegrationBase, DataIntegrationColumnBase, \
    DataIntegrationConnectionBase, \
    DataIntegrationConnectionDatabaseBase, DataIntegrationConnectionFileBase, DataIntegrationConnectionQueueBase, \
    DataIntegrationConnectionFileCsvBase
from process.domain.base.operation import DataOperationBase, DataOperationIntegrationBase
from process.domain.base.secret import SecretBase, SecretSourceBase, SecretSourceBasicAuthenticationBase
from process.domain.connection import Connection, ConnectionType, ConnectionDatabase, ConnectionFile, ConnectionQueue, \
    ConnectionServer, ConnectionSecret
from process.domain.dto.ConnectionBasicAuthentication import ConnectionBasicAuthentication
from process.domain.integration import DataIntegration, DataIntegrationColumn, DataIntegrationConnection, \
    DataIntegrationConnectionDatabase, DataIntegrationConnectionFile, DataIntegrationConnectionQueue, \
    DataIntegrationConnectionFileCsv
from process.domain.operation import DataOperation, DataOperationIntegration
from process.domain.secret import Secret, SecretSource, SecretSourceBasicAuthentication


class OperationCacheService(IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 crypto_service: CryptoService
                 ):
        self.crypto_service = crypto_service
        self.repository_provider = repository_provider
        self.data_operation: DataOperationBase = None
        self.data_operation_integrations: List[DataOperationIntegrationBase] = []
        self.data_integrations: List[DataIntegrationBase] = []
        self.data_integration_connections: List[DataIntegrationConnectionBase] = []
        self.connections: List[Connection] = []

    def load_entity(self, cls, entity):
        if entity is None:
            raise OperationalException(f"{cls.__name__} enitity is null")
        converter = BaseConverter(cls=cls)

        json_str = converter.ToJSON(entity)
        result = converter.FromJSON(json_str)
        return result

    def load_entities(self, cls, entities):
        converter = BaseConverter(cls=cls)
        result_list = []
        for entity in entities:
            json_str = converter.ToJSON(entity)
            result = converter.FromJSON(json_str)
            result_list.append(result)
        return result_list

    def get_data_operation_name(self, data_operation_id):
        data_operation_name = self.data_operation.Name
        return data_operation_name

    def get_data_operation_integrations_by_data_operation_id(self, data_operation_id) -> List[
        DataOperationIntegrationBase]:

        return self.data_operation.Integrations

    def get_data_operation_integration_by_id(self, data_operation_integration_id) -> DataOperationIntegrationBase:
        for data_operation_integration in self.data_operation_integrations:
            if data_operation_integration.Id == data_operation_integration_id:
                return data_operation_integration
        return None

    def get_data_integration_by_id(self, data_integration_id) -> DataIntegrationBase:
        for data_integration in self.data_integrations:
            if data_integration.Id == data_integration_id:
                return data_integration
        return None

    def get_data_integration_connection_by_id(self, data_integration_connection_id) -> DataIntegrationConnectionBase:
        for data_integration_connection in self.data_integration_connections:
            if data_integration_connection.Id == data_integration_connection_id:
                return data_integration_connection
        return None

    def get_source_connection(self, data_integration_id: int) -> DataIntegrationConnectionBase:

        for data_integration_connection in self.data_integration_connections:
            if data_integration_connection.DataIntegrationId == data_integration_id and data_integration_connection.SourceOrTarget == 0:
                return data_integration_connection
        return None

    def get_target_connection(self, data_integration_id: int) -> DataIntegrationConnectionBase:
        for data_integration_connection in self.data_integration_connections:
            if data_integration_connection.DataIntegrationId == data_integration_id and data_integration_connection.SourceOrTarget == 1:
                return data_integration_connection
        return None

    def get_columns_by_integration_id(self, data_integration_id) -> List[DataIntegrationColumnBase]:
        for data_integration in self.data_integrations:
            if data_integration.Id == data_integration_id:
                return data_integration.Columns
        return None

    def get_first_row(self, data_integration_id) -> DataIntegrationColumnBase:
        columns = self.get_columns_by_integration_id(data_integration_id)
        return columns[0]

    def get_connection_basic_authentication_by_connection_id(self, connection_id: int) -> ConnectionBasicAuthentication:
        connection = self.get_connection_by_id(connection_id=connection_id)
        secret_source_basic_authentication: SecretSourceBasicAuthentication = \
            connection.ConnectionSecrets[0].Secret.SecretSources[0].SecretSourceBasicAuthentications[0]

        connection_basic_authentication = ConnectionBasicAuthentication(
            User=self.crypto_service.decrypt(secret_source_basic_authentication.User),
            Password=self.crypto_service.decrypt(secret_source_basic_authentication.Password)
        )
        return connection_basic_authentication

    def get_connection_server_by_connection_id(self, connection_id: int) -> ConnectionServer:
        connection = self.get_connection_by_id(connection_id=connection_id)
        return connection.ConnectionServers[0]

    def get_connection_servers_by_connection_id(self, connection_id: int) -> ConnectionServer:
        connection = self.get_connection_by_id(connection_id=connection_id)
        return connection.ConnectionServers

    def get_connection_by_id(self, connection_id) -> ConnectionBase:
        for connection in self.connections:
            if connection.Id == connection_id:
                return connection
        return None

    def get_data_operation(self, data_operation_id) -> DataOperationBase:
        entity = self.repository_provider.create().session.execute(
            DataOperation.__table__.select().filter(
                DataOperation.IsDeleted == 0,
                DataOperation.Id == data_operation_id)).fetchone()
        result = self.load_entity(cls=DataOperationBase, entity=entity)
        return result

    def get_data_operation_integration(self, data_operation_integration_id) -> DataOperationIntegrationBase:
        entity = self.repository_provider.create().session.execute(
            DataOperationIntegration.__table__.select().filter(
                DataOperationIntegration.IsDeleted == 0,
                DataOperationIntegration.Id == data_operation_integration_id)).fetchone()

        result = self.load_entity(cls=DataOperationIntegrationBase, entity=entity)
        return result

    def get_data_operation_integrations(self, data_operation_id) -> List[DataOperationIntegrationBase]:
        entities = self.repository_provider.create().session.execute(
            DataOperationIntegration.__table__.select().filter(
                DataOperationIntegration.IsDeleted == 0,
                DataOperationIntegration.DataOperationId == data_operation_id).order_by(DataOperationIntegration.Order))
        result_list = self.load_entities(cls=DataOperationIntegrationBase, entities=entities)
        return result_list

    def get_data_integration(self, data_integration_id) -> DataIntegrationBase:
        entity = self.repository_provider.create().session.execute(
            DataIntegration.__table__.select().filter(

                DataIntegration.IsDeleted == 0,
                DataIntegration.Id == data_integration_id)).fetchone()
        result = self.load_entity(cls=DataIntegrationBase, entity=entity)
        return result

    def get_data_integration_columns(self, data_integration_id) -> List[DataIntegrationColumnBase]:
        entities = self.repository_provider.create().session.execute(
            DataIntegrationColumn.__table__.select().filter(
                DataIntegrationColumn.IsDeleted == 0,
                DataIntegrationColumn.DataIntegrationId == data_integration_id))

        result_list = self.load_entities(cls=DataIntegrationColumnBase, entities=entities)
        return result_list

    def get_data_integration_connections(self, data_integration_id) -> List[DataIntegrationConnectionBase]:
        entities = self.repository_provider.create().session.execute(
            DataIntegrationConnection.__table__.select().filter(
                DataIntegrationConnection.IsDeleted == 0,
                DataIntegrationConnection.DataIntegrationId == data_integration_id))

        result_list = self.load_entities(cls=DataIntegrationConnectionBase, entities=entities)
        return result_list

    def get_data_integration_connection_database(self,
                                                 data_integration_connection_id) -> DataIntegrationConnectionDatabaseBase:
        entity = self.repository_provider.create().session.execute(
            DataIntegrationConnectionDatabase.__table__.select().filter(
                DataIntegrationConnectionDatabase.IsDeleted == 0,
                DataIntegrationConnectionDatabase.DataIntegrationConnectionId == data_integration_connection_id)).fetchone()
        result = self.load_entity(cls=DataIntegrationConnectionDatabaseBase, entity=entity)
        return result

    def get_data_integration_connection_file(self, data_integration_connection_id) -> DataIntegrationConnectionFileBase:
        entity = self.repository_provider.create().session.execute(
            DataIntegrationConnectionFile.__table__.select().filter(
                DataIntegrationConnectionFile.IsDeleted == 0,
                DataIntegrationConnectionFile.DataIntegrationConnectionId == data_integration_connection_id)).fetchone()
        result = self.load_entity(cls=DataIntegrationConnectionFileBase, entity=entity)
        return result

    def get_data_integration_connection_file_csv(self,
                                                 data_integration_connection_file_id) -> DataIntegrationConnectionFileCsvBase:
        entity = self.repository_provider.create().session.execute(
            DataIntegrationConnectionFileCsv.__table__.select().filter(
                DataIntegrationConnectionFileCsv.IsDeleted == 0,
                DataIntegrationConnectionFileCsv.DataIntegrationConnectionId == data_integration_connection_file_id)).fetchone()
        result = self.load_entity(cls=DataIntegrationConnectionFileCsvBase, entity=entity)
        return result

    def get_data_integration_connection_queue(self,
                                              data_integration_connection_id) -> DataIntegrationConnectionQueueBase:
        entity = self.repository_provider.create().session.execute(
            DataIntegrationConnectionQueue.__table__.select().filter(
                DataIntegrationConnectionQueue.IsDeleted == 0,
                DataIntegrationConnectionQueue.DataIntegrationConnectionId == data_integration_connection_id)).fetchone()
        result = self.load_entity(cls=DataIntegrationConnectionQueueBase, entity=entity)
        return result

    def get_connection(self, connection_id) -> ConnectionBase:
        entity = self.repository_provider.create().session.execute(
            Connection.__table__.select().filter(
                Connection.IsDeleted == 0,
                Connection.Id == connection_id)).fetchone()
        if entity is None:
            raise OperationalException(f"Connection not found on execution. Connection Id :{connection_id}")
        result = self.load_entity(cls=ConnectionBase, entity=entity)
        return result

    def get_connection_type(self, connection_type_id) -> ConnectionTypeBase:
        entity = self.repository_provider.create().session.execute(
            ConnectionType.__table__.select().filter(
                ConnectionType.IsDeleted == 0,
                ConnectionType.Id == connection_type_id)).fetchone()
        if entity is None:
            raise OperationalException(
                f"Connection type not found on execution. Connection Type Id :{connection_type_id}")
        result = self.load_entity(cls=ConnectionTypeBase, entity=entity)
        return result

    def get_connection_servers(self, connection_id) -> List[ConnectionServerBase]:
        entities = self.repository_provider.create().session.execute(
            ConnectionServer.__table__.select().filter(
                ConnectionServer.IsDeleted == 0,
                ConnectionServer.ConnectionId == connection_id))

        if entities is None:
            raise OperationalException(f"Connection detail not found on execution. Connection Id :{connection_id}")
        result_list = self.load_entities(cls=ConnectionServerBase, entities=entities)
        return result_list

    def get_connection_secrets(self, connection_id) -> List[ConnectionSecretBase]:
        entities = self.repository_provider.create().session.execute(
            ConnectionSecret.__table__.select().filter(
                ConnectionSecret.IsDeleted == 0,
                ConnectionSecret.ConnectionId == connection_id))

        if entities is None:
            raise OperationalException(f"Connection detail not found on execution. Connection Id :{connection_id}")
        result_list = self.load_entities(cls=ConnectionSecretBase, entities=entities)
        return result_list

    def get_connection_database(self, connection_id) -> ConnectionDatabaseBase:
        entity = self.repository_provider.create().session.execute(
            ConnectionDatabase.__table__.select().filter(
                ConnectionDatabase.IsDeleted == 0,
                ConnectionDatabase.ConnectionId == connection_id)).fetchone()
        result = self.load_entity(cls=ConnectionDatabaseBase, entity=entity)
        return result

    def get_connection_file(self, connection_id) -> ConnectionFileBase:
        entity = self.repository_provider.create().session.execute(
            ConnectionFile.__table__.select().filter(
                ConnectionFile.IsDeleted == 0,
                ConnectionFile.ConnectionId == connection_id)).fetchone()
        result = self.load_entity(cls=ConnectionFileBase, entity=entity)
        return result

    def get_connection_queue(self, connection_id) -> ConnectionQueueBase:
        entity = self.repository_provider.create().session.execute(
            ConnectionQueue.__table__.select().filter(
                ConnectionQueue.IsDeleted == 0,
                ConnectionQueue.ConnectionId == connection_id)).fetchone()
        result = self.load_entity(cls=ConnectionQueueBase, entity=entity)
        return result

    def get_secret(self, secret_id) -> SecretBase:
        entity = self.repository_provider.create().session.execute(
            Secret.__table__.select().filter(
                Secret.IsDeleted == 0,
                Secret.Id == secret_id)).fetchone()
        result = self.load_entity(cls=SecretBase, entity=entity)
        return result

    def get_secret_sources(self, secret_id) -> List[SecretSourceBase]:
        entities = self.repository_provider.create().session.execute(
            SecretSource.__table__.select().filter(
                SecretSource.IsDeleted == 0,
                SecretSource.SecretId == secret_id))
        result_list = self.load_entities(cls=SecretSourceBase, entities=entities)
        return result_list

    def get_secret_source_basic_authentications(self, secret_source_id) -> List[SecretSourceBasicAuthenticationBase]:
        entities = self.repository_provider.create().session.execute(
            SecretSourceBasicAuthentication.__table__.select().filter(
                SecretSourceBasicAuthentication.IsDeleted == 0,
                SecretSourceBasicAuthentication.SecretSourceId == secret_source_id))
        result_list = self.load_entities(cls=SecretSourceBasicAuthenticationBase, entities=entities)
        return result_list

    def initialize_connection(self, connection_id):
        connection = self.get_connection_by_id(connection_id=connection_id)
        if connection is not None:
            return connection

        connection = self.get_connection(connection_id=connection_id)
        connection.ConnectionServers = self.get_connection_servers(connection_id=connection_id)
        connection.ConnectionType = self.get_connection_type(connection_type_id=connection.ConnectionTypeId)
        if connection.ConnectionTypeId == ConnectionTypes.Database.value:
            connection.Database = self.get_connection_database(connection_id=connection_id)
        if connection.ConnectionTypeId == ConnectionTypes.File.value:
            connection.File = self.get_connection_file(connection_id=connection_id)
        if connection.ConnectionTypeId == ConnectionTypes.Queue.value:
            connection.Queue = self.get_connection_queue(connection_id=connection_id)

        connection.ConnectionSecrets = self.get_connection_secrets(connection_id=connection_id)
        for connection_secret in connection.ConnectionSecrets:
            connection_secret.Secret = self.get_secret(secret_id=connection_secret.SecretId)
            connection_secret.Secret.SecretSources = self.get_secret_sources(secret_id=connection_secret.SecretId)
            for secret_source in connection_secret.Secret.SecretSources:
                secret_source.SecretSourceBasicAuthentications = self.get_secret_source_basic_authentications(
                    secret_source_id=secret_source.Id)

        self.connections.append(connection)
        return connection

    def initialize_data_integation(self, data_integration_id):
        data_integration = self.get_data_integration(
            data_integration_id=data_integration_id)
        data_integration.Columns = self.get_data_integration_columns(
            data_integration_id=data_integration_id)
        data_integration.Connections = self.get_data_integration_connections(
            data_integration_id=data_integration_id)

        for data_integration_connection in data_integration.Connections:
            data_integration_connection.Connection = self.initialize_connection(
                connection_id=data_integration_connection.ConnectionId)
            if data_integration_connection.Connection.ConnectionTypeId == ConnectionTypes.Database.value:
                data_integration_connection.Database = self.get_data_integration_connection_database(
                    data_integration_connection_id=data_integration_connection.Id)
            if data_integration_connection.Connection.ConnectionTypeId == ConnectionTypes.File.value:
                data_integration_connection.File = self.get_data_integration_connection_file(
                    data_integration_connection_id=data_integration_connection.Id)
                data_integration_connection.File.Csv = self.get_data_integration_connection_file_csv(
                    data_integration_connection_file_id=data_integration_connection.File.Id)
            if data_integration_connection.Connection.ConnectionTypeId == ConnectionTypes.Queue.value:
                data_integration_connection.Queue = self.get_data_integration_connection_queue(
                    data_integration_connection_id=data_integration_connection.Id)
            self.data_integration_connections.append(data_integration_connection)

        self.data_integrations.append(data_integration)
        return data_integration

    def initialize_data_operation_integation(self, data_operation_integration_id):
        data_operation_integration = self.get_data_operation_integration(
            data_operation_integration_id=data_operation_integration_id)
        data_operation_integration.DataIntegration = self.initialize_data_integation(
            data_integration_id=data_operation_integration.DataIntegrationId)

        self.data_operation_integrations.append(data_operation_integration)
        return data_operation_integration

    @transactionhandler
    def create_data_operation_integration(self, data_operation_integration_id):
        self.get_data_operation_integration(data_operation_integration_id=data_operation_integration_id)

    @transactionhandler
    def create_data_integration(self, data_integration_id):
        self.initialize_data_integation(data_integration_id=data_integration_id)

    @transactionhandler
    def create(self, data_operation_id):

        self.data_operation = self.get_data_operation(data_operation_id=data_operation_id)
        self.data_operation.Integrations = []
        data_operation_integrations = self.get_data_operation_integrations(data_operation_id=data_operation_id)
        for data_operation_integration in data_operation_integrations:
            doi = self.initialize_data_operation_integation(data_operation_integration_id=data_operation_integration.Id)
            self.data_operation.Integrations.append(doi)
        self.repository_provider.commit()
        return self.data_operation
