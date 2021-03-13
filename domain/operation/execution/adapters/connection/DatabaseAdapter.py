from typing import List

from injector import inject

from domain.integration.services.DataIntegrationColumnService import DataIntegrationColumnService
from domain.integration.services.DataIntegrationConnectionService import DataIntegrationConnectionService
from infrastructor.connection.database.DatabaseProvider import DatabaseProvider
from infrastructor.connection.adapters.ConnectionAdapter import ConnectionAdapter
from models.dto.LimitModifier import LimitModifier


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
        target_connection_manager = self.database_provider.get_database_context(
            connection=target_connection.Connection)
        truncate_affected_rowcount = target_connection_manager.truncate_table(schema=target_connection.Schema,
                                                                              table=target_connection.TableName)
        return truncate_affected_rowcount

    def get_source_data_count(self, data_integration_id) -> int:
        source_connection = self.data_integration_connection_service.get_source_connection(
            data_integration_id=data_integration_id)

        source_connection_manager = self.database_provider.get_database_context(
            connection=source_connection.Connection)
        data_count = source_connection_manager.get_table_count(source_connection.Query)
        return data_count

    def get_source_data(self, data_integration_id: int, limit_modifier: LimitModifier) -> List[any]:
        source_connection = self.data_integration_connection_service.get_source_connection(
            data_integration_id=data_integration_id)
        source_connection_manager = self.database_provider.get_database_context(
            connection=source_connection.Connection)
        first_row = self.data_integration_column_service.get_first_row(data_integration_id=data_integration_id)
        extracted_data = source_connection_manager.get_table_data(
            query=source_connection.Query,
            first_row=f'"{first_row.SourceColumnName}"',
            sub_limit=limit_modifier.SubLimit,
            top_limit=limit_modifier.TopLimit
        )
        return extracted_data

    def prepare_data(self, data_integration_id: int, source_data: List[any]) -> List[any]:
        target_connection = self.data_integration_connection_service.get_target_connection(
            data_integration_id=data_integration_id)

        target_connection_manager = self.database_provider.get_database_context(connection=target_connection.Connection)

        data_integration_columns = self.data_integration_column_service.get_columns_by_integration_id(
            data_integration_id=data_integration_id)

        column_rows = [(data_integration_column.ResourceType, data_integration_column.SourceColumnName,
                        data_integration_column.TargetColumnName) for data_integration_column in
                       data_integration_columns]
        prepared_data = target_connection_manager.prepare_insert_row(extracted_datas=source_data,
                                                                     column_rows=column_rows)
        return prepared_data

    def prepare_target_query(self, data_integration_id: int) -> str:
        target_connection = self.data_integration_connection_service.get_target_connection(
            data_integration_id=data_integration_id)

        target_connection_manager = self.database_provider.get_database_context(connection=target_connection.Connection)

        data_integration_columns = self.data_integration_column_service.get_columns_by_integration_id(
            data_integration_id=data_integration_id)

        column_rows = [(data_integration_column.ResourceType, data_integration_column.SourceColumnName,
                        data_integration_column.TargetColumnName) for data_integration_column in
                       data_integration_columns]
        prepared_target_query = target_connection_manager.prepare_target_query(
            column_rows=column_rows,
            query=target_connection.Query)
        return prepared_target_query

    def write_target_data(self, data_integration_id: int, prepared_data: List[any], ) -> int:
        target_connection = self.data_integration_connection_service.get_target_connection(
            data_integration_id=data_integration_id)

        target_connection_manager = self.database_provider.get_database_context(connection=target_connection.Connection)

        prepared_target_query = self.prepare_target_query(data_integration_id=data_integration_id)
        # rows insert to database
        affected_row_count = target_connection_manager.execute_many(query=prepared_target_query, data=prepared_data)
        return affected_row_count

    def do_target_operation(self, data_integration_id: int) -> int:
        target_connection = self.data_integration_connection_service.get_target_connection(
            data_integration_id=data_integration_id)
        target_connection_manager = self.database_provider.get_database_context(
            connection=target_connection.Connection)

        affected_rowcount = target_connection_manager.execute(query=target_connection.Query)

        return affected_rowcount
