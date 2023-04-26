from typing import List

from injector import inject
from pdip.integrator.connection.domain.base import ConnectionColumnBase
from pdip.integrator.connection.domain.enums import ConnectionTypes
from pdip.integrator.connection.domain.types.sql.base import ConnectionSqlBase
from pdip.integrator.integration.domain.base import IntegrationBase, IntegrationConnectionBase
from pdip.integrator.operation.domain import OperationIntegrationBase, OperationBase

from pdip.integrator.connection.domain.types.bigdata.base import ConnectionBigDataBase
from src.application.integrator.OperationCacheService import OperationCacheService
from src.application.integrator.converters.ConnectionConverter import ConnectionConverter
from src.domain.base.connection import ConnectionBase
from src.domain.base.integration import DataIntegrationBase, DataIntegrationConnectionBase
from src.domain.base.operation import DataOperationBase


class OperationConverter:
    @inject
    def __init__(
            self,
            connection_converter: ConnectionConverter,
            operation_cache_service: OperationCacheService
    ):
        self.connection_converter = connection_converter
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

                    operation_integration.Integration.SourceConnections = self.convert_integration_connection(
                        data_integration=data_integration,
                        data_integration_connection=data_integration_connection,
                        connection=connection
                    )
                else:
                    operation_integration.Integration.TargetConnections = self.convert_integration_connection(
                        data_integration=data_integration,
                        data_integration_connection=data_integration_connection,
                        connection=connection
                    )

            operation.Integrations.append(operation_integration)
        return operation

    def convert_integration_connection(
            self,
            data_integration: DataIntegrationBase,
            data_integration_connection: DataIntegrationConnectionBase,
            connection: ConnectionBase
    ) -> IntegrationConnectionBase:
        integration_connection = IntegrationConnectionBase(
            ConnectionName=connection.Name,
            ConnectionType=ConnectionTypes(connection.ConnectionType.Id)
        )
        if integration_connection.ConnectionType == ConnectionTypes.Sql:
            connection_sql = self.connection_converter.convert_connection_sql(connection=connection)
            integration_connection.Sql = ConnectionSqlBase(
                Connection=connection_sql,
                Schema=data_integration_connection.Database.Schema,
                ObjectName=data_integration_connection.Database.TableName,
                Query=data_integration_connection.Database.Query
            )
            integration_connection.Columns = self.convert_connection_columns(data_integration=data_integration)
        elif integration_connection.ConnectionType == ConnectionTypes.BigData:
            connection_big_data = self.connection_converter.convert_connection_big_data(connection=connection)
            integration_connection.BigData = ConnectionBigDataBase(
                Connection=connection_big_data,
                Schema=data_integration_connection.BigData.Schema,
                ObjectName=data_integration_connection.BigData.TableName,
                Query=data_integration_connection.BigData.Query
            )
            integration_connection.Columns = self.convert_connection_columns(data_integration=data_integration)
        return integration_connection

    def convert_connection_columns(self, data_integration: DataIntegrationBase) -> List[
        ConnectionColumnBase]:
        if data_integration.Columns is not None and len(data_integration.Columns) > 0:
            integration_connection_columns = []
            for data_integration_column in data_integration.Columns:
                column = ConnectionColumnBase(
                    Name=data_integration_column.SourceColumnName)
                integration_connection_columns.append(column)
            return integration_connection_columns
        return None

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
