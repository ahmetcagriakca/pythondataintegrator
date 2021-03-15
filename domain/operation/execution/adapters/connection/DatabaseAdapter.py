from typing import List

from injector import inject

from domain.integration.services.DataIntegrationColumnService import DataIntegrationColumnService
from domain.integration.services.DataIntegrationConnectionService import DataIntegrationConnectionService
from infrastructor.connection.database.DatabaseProvider import DatabaseProvider
from infrastructor.connection.adapters.ConnectionAdapter import ConnectionAdapter
from models.dto.PagingModifier import PagingModifier


class DatabaseAdapter(ConnectionAdapter):
    @inject
    def __init__(self,
                 database_provider: DatabaseProvider,
                 data_integration_connection_service: DataIntegrationConnectionService,
                 data_integration_column_service: DataIntegrationColumnService,
                 ):
        self.data_integration_column_service = data_integration_column_service
        self.data_integration_connection_service = data_integration_connection_service
        self.database_provider = database_provider

    def clear_data(self, data_integration_id) -> int:
        target_connection = self.data_integration_connection_service.get_target_connection(
            data_integration_id=data_integration_id)
        target_database_context = self.database_provider.get_database_context(
            connection=target_connection.Connection)
        truncate_affected_rowcount = target_database_context.truncate_table(schema=target_connection.Database.Schema,
                                                                              table=target_connection.Database.TableName)
        return truncate_affected_rowcount

    def get_source_data_count(self, data_integration_id) -> int:
        source_connection = self.data_integration_connection_service.get_source_connection(
            data_integration_id=data_integration_id)

        source_database_context = self.database_provider.get_database_context(
            connection=source_connection.Connection)
        data_count = source_database_context.get_table_count(source_connection.Database.Query)
        return data_count

    def get_source_data(self, data_integration_id: int, paging_modifier: PagingModifier) -> List[any]:
        source_connection = self.data_integration_connection_service.get_source_connection(
            data_integration_id=data_integration_id)
        source_database_context = self.database_provider.get_database_context(
            connection=source_connection.Connection)
        first_row = self.data_integration_column_service.get_first_row(data_integration_id=data_integration_id)
        data = source_database_context.get_table_data(
            query=source_connection.Database.Query,
            first_row=f'"{first_row.SourceColumnName}"',
            start=paging_modifier.Start,
            end=paging_modifier.End
        )
        return data

    def prepare_data(self, data_integration_id: int, source_data: List[any]) -> List[any]:
        target_connection = self.data_integration_connection_service.get_target_connection(
            data_integration_id=data_integration_id)

        target_database_context = self.database_provider.get_database_context(connection=target_connection.Connection)

        data_integration_columns = self.data_integration_column_service.get_columns_by_integration_id(
            data_integration_id=data_integration_id)

        column_rows = [(data_integration_column.ResourceType, data_integration_column.SourceColumnName,
                        data_integration_column.TargetColumnName) for data_integration_column in
                       data_integration_columns]
        prepared_data = target_database_context.prepare_insert_row(data=source_data,
                                                                     column_rows=column_rows)
        return prepared_data

    def prepare_target_query(self, data_integration_id: int) -> str:
        target_connection = self.data_integration_connection_service.get_target_connection(
            data_integration_id=data_integration_id)

        target_database_context = self.database_provider.get_database_context(connection=target_connection.Connection)

        data_integration_columns = self.data_integration_column_service.get_columns_by_integration_id(
            data_integration_id=data_integration_id)

        column_rows = [(data_integration_column.ResourceType, data_integration_column.SourceColumnName,
                        data_integration_column.TargetColumnName) for data_integration_column in
                       data_integration_columns]
        prepared_target_query = target_database_context.prepare_target_query(
            column_rows=column_rows,
            query=target_connection.Database.Query)
        return prepared_target_query

    def write_target_data(self, data_integration_id: int, prepared_data: List[any], ) -> int:
        target_connection = self.data_integration_connection_service.get_target_connection(
            data_integration_id=data_integration_id)

        target_database_context = self.database_provider.get_database_context(connection=target_connection.Connection)

        prepared_target_query = self.prepare_target_query(data_integration_id=data_integration_id)
        # rows insert to database
        affected_row_count = target_database_context.execute_many(query=prepared_target_query, data=prepared_data)
        return affected_row_count

    def do_target_operation(self, data_integration_id: int) -> int:
        target_connection = self.data_integration_connection_service.get_target_connection(
            data_integration_id=data_integration_id)
        target_database_context = self.database_provider.get_database_context(
            connection=target_connection.Connection)

        affected_rowcount = target_database_context.execute(query=target_connection.Database.Query)

        return affected_rowcount
