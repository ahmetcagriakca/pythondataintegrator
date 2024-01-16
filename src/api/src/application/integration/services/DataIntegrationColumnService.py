from typing import List

from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped
from pdip.exceptions import OperationalException
from pdip.integrator.connection.domain.base import ConnectionColumnBase
from pdip.integrator.connection.domain.enums import ConnectorTypes, ConnectionTypes
from pdip.integrator.connection.types.bigdata.base import BigDataProvider
from pdip.integrator.connection.types.sql.base import SqlProvider

from src.domain.connection.Connection import Connection
from src.domain.integration.DataIntegration import DataIntegration
from src.domain.integration.DataIntegrationColumn import DataIntegrationColumn


class DataIntegrationColumnService(IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        self.data_integration_column_repository = repository_provider.get(DataIntegrationColumn)

    #######################################################################################

    def get_by_id(self, id: int) -> DataIntegrationColumn:
        entity = self.data_integration_column_repository.first(IsDeleted=0, Id=id)
        return entity

    def get_first_row(self, data_integration_id) -> DataIntegrationColumn:
        entity = self.data_integration_column_repository.first(IsDeleted=0, DataIntegrationId=data_integration_id)
        return entity

    def get_columns_by_integration_id(self, data_integration_id) -> DataIntegrationColumn:
        entities = self.data_integration_column_repository.filter_by(IsDeleted=0,
                                                                     DataIntegrationId=data_integration_id).all()
        return entities

    def get_source_query(self, connection: Connection, data_integration: DataIntegration, schema: str, table_name: str):

        data_integration_columns = self.data_integration_column_repository.filter_by(IsDeleted=0,
                                                                                     DataIntegration=data_integration)

        query = None
        if data_integration_columns is not None and len(data_integration_columns) > 0:

            column_rows = [ConnectionColumnBase(Name=data_integration_column.SourceColumnName,
                                                Type=data_integration_column.ResourceType)
                           for data_integration_column in data_integration_columns]
            if connection.ConnectionType.Id == ConnectionTypes.Sql.value:
                context = SqlProvider().get_context(
                    connector_type=ConnectorTypes(connection.Database.ConnectorTypeId),
                    host=connection.ConnectionServers[0].Host,
                    port=connection.ConnectionServers[0].Port,
                    user=None,
                    password=None,
                    database=connection.Database.DatabaseName,
                    service_name=connection.Database.ServiceName,
                    sid=connection.Database.Sid
                )
                query = context.dialect.prepare_select_query(schema=schema, table=table_name, columns=column_rows)
            elif connection.ConnectionType.Id == ConnectionTypes.BigData.value:
                context = BigDataProvider().get_context(
                    connector_type=ConnectorTypes(connection.Database.ConnectorTypeId),
                    host=connection.ConnectionServers[0].Host,
                    port=connection.ConnectionServers[0].Port,
                    user=None,
                    password=None,
                    database=connection.Database.DatabaseName,
                    service_name=connection.Database.ServiceName,
                    sid=connection.Database.Sid
                )
                query = context.dialect.get(schema=schema, table_name=table_name, columns=column_rows)
        return query

    def get_target_query(self, connection: Connection, data_integration: DataIntegration, schema: str, table_name: str):

        data_integration_columns = self.data_integration_column_repository.filter_by(IsDeleted=0,
                                                                                     DataIntegration=data_integration)

        query = None
        if data_integration_columns is not None and data_integration_columns.count() > 0:
            source_column_rows = [ConnectionColumnBase(Name=data_integration_column.SourceColumnName,
                                                       Type=data_integration_column.ResourceType)
                                  for data_integration_column in data_integration_columns]
            target_column_rows = [ConnectionColumnBase(Name=data_integration_column.TargetColumnName,
                                                       Type=data_integration_column.ResourceType)
                                  for data_integration_column in data_integration_columns]
            if connection.ConnectionType.Id == ConnectionTypes.Sql.value:
                context = SqlProvider().get_context(
                    connector_type=ConnectorTypes(connection.Database.ConnectorTypeId),
                    host=connection.ConnectionServers[0].Host,
                    port=connection.ConnectionServers[0].Port,
                    user=None,
                    password=None,
                    database=connection.Database.DatabaseName,
                    service_name=connection.Database.ServiceName,
                    sid=connection.Database.Sid
                )
                query = context.generate_insert_query(
                    source_columns=source_column_rows,
                    target_columns=target_column_rows,
                    schema=schema,
                    table=table_name
                )
            elif connection.ConnectionType.Id == ConnectionTypes.BigData.value:
                context = BigDataProvider().get_context(
                    connector_type=ConnectorTypes(connection.Database.ConnectorTypeId),
                    host=connection.ConnectionServers[0].Host,
                    port=connection.ConnectionServers[0].Port,
                    user=None,
                    password=None,
                    database=connection.Database.DatabaseName,
                    service_name=connection.Database.ServiceName,
                    sid=connection.Database.Sid
                )
                query = context.generate_insert_query(
                    source_columns=source_column_rows,
                    target_columns=target_column_rows,
                    schema=schema,
                    table=table_name
                )
        return query

    def insert(self,
               data_integration: DataIntegration,
               source_columns: str,
               target_columns: str) -> List[DataIntegrationColumn]:

        source_columns_list = source_columns.split(",")
        target_columns_list = target_columns.split(",")
        if len(source_columns_list) != len(target_columns_list):
            raise OperationalException("Source and Target Column List must be equal")
        data_integration_columns: List[DataIntegrationColumn] = []
        for source_column in source_columns_list:
            target_column = target_columns_list[source_columns_list.index(source_column)]
            source_column_name = source_column.strip()
            target_column_name = target_column.strip()
            data_integration_column = DataIntegrationColumn(SourceColumnName=source_column_name,
                                                            TargetColumnName=target_column_name,
                                                            DataIntegration=data_integration)
            data_integration_columns.append(data_integration_column)
            self.data_integration_column_repository.insert(data_integration_column)
        return data_integration_columns

    def update(self,
               data_integration: DataIntegration,
               source_columns: str,
               target_columns: str) -> List[DataIntegrationColumn]:
        source_columns_list = source_columns.split(",")
        target_columns_list = target_columns.split(",")

        if len(source_columns_list) != len(target_columns_list):
            raise OperationalException("Source and Target Column List must be equal")

        data_integration_columns = self.data_integration_column_repository.filter_by(
            DataIntegration=data_integration)
        for data_integration_column in data_integration_columns:
            self.repository_provider.create().session.delete(data_integration_column)

        source_columns_list = source_columns.split(",")
        target_columns_list = target_columns.split(",")
        if len(source_columns_list) != len(target_columns_list):
            raise OperationalException("Source and Target Column List must be equal")
        data_integration_columns: List[DataIntegrationColumn] = []
        for source_column in source_columns_list:
            target_column = target_columns_list[source_columns_list.index(source_column)]
            source_column_name = source_column.strip()
            target_column_name = target_column.strip()
            data_integration_column = DataIntegrationColumn(SourceColumnName=source_column_name,
                                                            TargetColumnName=target_column_name,
                                                            DataIntegration=data_integration)
            data_integration_columns.append(data_integration_column)
            self.data_integration_column_repository.insert(data_integration_column)
        return data_integration

    def delete(self, id: int):
        self.data_integration_column_repository.delete_by_id(id)
