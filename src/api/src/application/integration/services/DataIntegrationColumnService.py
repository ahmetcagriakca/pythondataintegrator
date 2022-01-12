from typing import List

from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped
from pdip.exceptions import OperationalException
from pdip.integrator.connection.domain.enums import ConnectorTypes, ConnectionTypes

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

        column_rows = [(data_integration_column.ResourceType, data_integration_column.SourceColumnName,
                        data_integration_column.TargetColumnName) for data_integration_column in
                       data_integration_columns]
        selected_rows = ""
        if connection.ConnectionType.Id == ConnectionTypes.Sql.value:
            if connection.Database.ConnectorTypeId == ConnectorTypes.MYSQL.value:
                for column_row in column_rows:
                    selected_rows += f'{"" if column_row == column_rows[0] else ", "}`{column_row[1].strip()}`'
                query = f'SELECT {selected_rows} FROM `{schema}`.`{table_name}`'

            else:
                for column_row in column_rows:
                    selected_rows += f'{"" if column_row == column_rows[0] else ", "}"{column_row[1].strip()}"'
                query = f'SELECT {selected_rows} FROM "{schema}"."{table_name}"'
        elif connection.ConnectionType.Id == ConnectionTypes.BigData.value:
            for column_row in column_rows:
                selected_rows += f'{"" if column_row == column_rows[0] else ", "}{column_row[1].strip()}'
            query = f'SELECT {selected_rows} FROM {schema}.{table_name}'
        return query

    def get_target_query(self, connection: Connection, data_integration: DataIntegration, schema: str, table_name: str):

        data_integration_columns = self.data_integration_column_repository.filter_by(IsDeleted=0,
                                                                                     DataIntegration=data_integration)
        insert_row_columns = ""
        insert_row_values = ""
        if connection.ConnectionType.Id == ConnectionTypes.Sql.value:
            if connection.Database.ConnectorTypeId == ConnectorTypes.MYSQL.value:
                for column in data_integration_columns:
                    insert_row_columns += f'{"" if column == data_integration_columns[0] else ", "}`{column.TargetColumnName}`'
                    insert_row_values += f'{"" if column == data_integration_columns[0] else ", "}:{column.SourceColumnName}'
                query = f'INSERT INTO `{schema}`.`{table_name}`({insert_row_columns}) VALUES ({insert_row_values})'
            else:
                for column in data_integration_columns:
                    insert_row_columns += f'{"" if column == data_integration_columns[0] else ", "}"{column.TargetColumnName}"'
                    insert_row_values += f'{"" if column == data_integration_columns[0] else ", "}:{column.SourceColumnName}'
                query = f'INSERT INTO "{schema}"."{table_name}"({insert_row_columns}) VALUES ({insert_row_values})'
        elif connection.ConnectionType.Id == ConnectionTypes.BigData.value:
            for column in data_integration_columns:
                insert_row_columns += f'{"" if column == data_integration_columns[0] else ", "}{column.TargetColumnName}'
                insert_row_values += f'{"" if column == data_integration_columns[0] else ", "}:{column.SourceColumnName}'
            query = f'INSERT INTO {schema}.{table_name}({insert_row_columns}) VALUES ({insert_row_values})'
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
        for relatedColumn in source_columns_list:
            target_column_name = target_columns_list[source_columns_list.index(relatedColumn)]
            data_integration_column = DataIntegrationColumn(SourceColumnName=relatedColumn,
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
        for source_column_name_data in source_columns_list:
            target_column_name_data = target_columns_list[source_columns_list.index(source_column_name_data)]
            source_column_name = source_column_name_data.strip()
            target_column_name = target_column_name_data.strip()
            data_integration_column = self.data_integration_column_repository.first(
                SourceColumnName=source_column_name, TargetColumnName=target_column_name,
                DataIntegration=data_integration)
            if data_integration_column is None:
                data_integration_column = DataIntegrationColumn(
                    SourceColumnName=source_column_name,
                    TargetColumnName=target_column_name,
                    DataIntegration=data_integration)
                self.data_integration_column_repository.insert(data_integration_column)
        for data_integration_column in data_integration.Columns:
            column_found = False
            source_columns = [source_column for source_column in source_columns_list if
                              source_column == data_integration_column.SourceColumnName]
            source_column_name = None
            if source_columns is not None and len(source_columns) > 0:
                source_column_name = source_columns[0]
            if source_column_name is not None:
                target_column_name = target_columns_list[source_columns_list.index(source_column_name)]
                if target_column_name == data_integration_column.TargetColumnName:
                    column_found = True
            if not column_found:
                self.repository_provider.create().session.delete(data_integration_column)
        return data_integration

    def delete(self, id: int):
        self.data_integration_column_repository.delete_by_id(id)
