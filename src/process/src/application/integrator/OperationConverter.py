from injector import inject
from pdip.integrator.connection.domain.authentication.basic import BasicAuthentication
from pdip.integrator.connection.domain.enums import ConnectionTypes, ConnectorTypes
from pdip.integrator.connection.domain.server.base import Server
from pdip.integrator.connection.domain.sql import SqlConnectionConfiguration
from pdip.integrator.integration.domain.base import IntegrationConnectionSqlBase, IntegrationConnectionColumnBase, \
    IntegrationConnectionBase, IntegrationBase
from pdip.integrator.operation.domain import OperationIntegrationBase, OperationBase

from src.application.integrator.OperationCacheService import OperationCacheService
from src.domain.base.operation import DataOperationBase


class OperationConverter:
    @inject
    def __init__(self, operation_cache_service: OperationCacheService):
        self.operation_cache_service = operation_cache_service

    def convert(self, data_operation_id):
        self.operation_cache_service.create(data_operation_id=data_operation_id)
        data_operation: DataOperationBase = self.operation_cache_service.data_operation

        operation = OperationBase(
            Id=data_operation.Id,
            Name=data_operation.Name,
            Integrations=[]
        )
        data_operation_integrations = self.operation_cache_service.data_operation_integrations
        for data_operation_integration in data_operation_integrations:
            operation_integration = OperationIntegrationBase(
                Id=data_operation_integration.Id,
                Name=data_operation_integration.DataIntegration.Code,
                Order=data_operation_integration.Order,
                Limit=data_operation_integration.Limit,
                ProcessCount=data_operation_integration.ProcessCount
            )
            data_integration = data_operation_integration.DataIntegration
            operation_integration.Integration = IntegrationBase(
                IsTargetTruncate=data_operation_integration.DataIntegration.IsTargetTruncate
            )
            for data_integration_connection in data_operation_integration.DataIntegration.Connections:
                connection = self.operation_cache_service.get_connection_by_id(data_integration_connection.ConnectionId)
                if data_integration_connection.SourceOrTarget == 0:
                    operation_integration.Integration.SourceConnections = IntegrationConnectionBase(
                        ConnectionName=connection.Name,
                        ConnectionType=ConnectionTypes(connection.ConnectionType.Id)
                    )
                    if operation_integration.Integration.SourceConnections.ConnectionType == ConnectionTypes.Sql:

                        connection_basic_authentication = self.operation_cache_service.get_connection_basic_authentication_by_connection_id(
                            connection_id=connection.Id)
                        connection_server = self.operation_cache_service.get_connection_server_by_connection_id(
                            connection_id=connection.Id)
                        connection_sql = SqlConnectionConfiguration(
                            Name=connection.Name,
                            ConnectionType=ConnectionTypes.Sql,
                            ConnectorType=ConnectorTypes(connection.Database.ConnectorTypeId),
                            Server=Server(
                                Host=connection_server.Host,
                                Port=connection_server.Port
                            ),
                            BasicAuthentication=BasicAuthentication(
                                User=connection_basic_authentication.User,
                                Password=connection_basic_authentication.Password
                            ),
                            Database=connection.Database.DatabaseName,
                            ServiceName=connection.Database.ServiceName,
                            Sid=connection.Database.Sid,
                        )
                        operation_integration.Integration.SourceConnections.Sql = IntegrationConnectionSqlBase(
                            Connection=connection_sql,
                            Schema=data_integration_connection.Database.Schema,
                            ObjectName=data_integration_connection.Database.TableName,
                            Query=data_integration_connection.Database.Query
                        )
                        if data_integration.Columns is not None and len(data_integration.Columns) > 0:
                            operation_integration.Integration.SourceConnections.Columns = []
                            for data_integration_column in data_integration.Columns:
                                column = IntegrationConnectionColumnBase(
                                    Name=data_integration_column.SourceColumnName)
                                operation_integration.Integration.SourceConnections.Columns.append(column)
                else:
                    operation_integration.Integration.TargetConnections = IntegrationConnectionBase(
                        ConnectionName=connection.Name,
                        ConnectionType=ConnectionTypes(connection.ConnectionType.Id)
                    )
                    if operation_integration.Integration.TargetConnections.ConnectionType == ConnectionTypes.Sql:
                        connection_basic_authentication = self.operation_cache_service.get_connection_basic_authentication_by_connection_id(
                            connection_id=connection.Id)
                        connection_server = self.operation_cache_service.get_connection_server_by_connection_id(
                            connection_id=connection.Id)
                        connection_sql = SqlConnectionConfiguration(
                            Name=connection.Name,
                            ConnectionType=ConnectionTypes.Sql,
                            ConnectorType=ConnectorTypes(connection.Database.ConnectorTypeId),
                            Server=Server(
                                Host=connection_server.Host,
                                Port=connection_server.Port
                            ),
                            BasicAuthentication=BasicAuthentication(
                                User=connection_basic_authentication.User,
                                Password=connection_basic_authentication.Password
                            ),
                            Database=connection.Database.DatabaseName,
                            ServiceName=connection.Database.ServiceName,
                            Sid=connection.Database.Sid,
                        )
                        operation_integration.Integration.TargetConnections.Sql = IntegrationConnectionSqlBase(
                            Connection=connection_sql,
                            Schema=data_integration_connection.Database.Schema,
                            ObjectName=data_integration_connection.Database.TableName,
                            Query=data_integration_connection.Database.Query
                        )
                        if data_integration.Columns is not None and len(data_integration.Columns) > 0:
                            operation_integration.Integration.TargetConnections.Columns = []
                            for data_integration_column in data_integration.Columns:
                                column = IntegrationConnectionColumnBase(
                                    Name=data_integration_column.TargetColumnName)
                                operation_integration.Integration.TargetConnections.Columns.append(column)

            operation.Integrations.append(operation_integration)
        return operation

    def print(self, operation):
        self.logger.info(f'operation.Name:{operation.Name}')
        for operation_integration in operation.Integrations:

            self.logger.info(f'operation_integration.Order:{operation_integration.Order}')
            self.logger.info(f'operation_integration.Limit:{operation_integration.Limit}')
            self.logger.info(f'operation_integration.ProcessCount:{operation_integration.ProcessCount}')
            self.logger.info(
                f'operation_integration.TargetConnections.Sql.Connection.Name:{operation_integration.Integration.TargetConnections.Sql.Connection.Name}')
            self.logger.info(
                f'operation_integration.TargetConnections.Sql.Schema:{operation_integration.Integration.TargetConnections.Sql.Schema}')
            self.logger.info(
                f'operation_integration.TargetConnections.Sql.ObjectName:{operation_integration.Integration.TargetConnections.Sql.ObjectName}')
            self.logger.info(
                f'operation_integration.TargetConnections.Sql.Query:{operation_integration.Integration.TargetConnections.Sql.Query}')
            if operation_integration.Integration.TargetConnections.Columns is not None:
                self.logger.info(
                    f'operation_integration.target_column_count:{len(operation_integration.Integration.TargetConnections.Columns)}')
