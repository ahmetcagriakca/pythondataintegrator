import json
from asyncio import Queue
from typing import List
from injector import inject
from pandas import DataFrame

from domain.integration.services.DataIntegrationColumnService import DataIntegrationColumnService
from domain.integration.services.DataIntegrationConnectionService import DataIntegrationConnectionService
from infrastructor.connection.database.DatabaseProvider import DatabaseProvider
from infrastructor.connection.adapters.ConnectionAdapter import ConnectionAdapter
from infrastructor.connection.models.DataQueueTask import DataQueueTask
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
        target_context = self.database_provider.get_context(connection=target_connection.Connection)
        truncate_affected_rowcount = target_context.truncate_table(schema=target_connection.Database.Schema,
                                                                   table=target_connection.Database.TableName)
        return truncate_affected_rowcount

    def get_source_data_count(self, data_integration_id) -> int:
        source_connection = self.data_integration_connection_service.get_source_connection(
            data_integration_id=data_integration_id)

        source_context = self.database_provider.get_context(
            connection=source_connection.Connection)
        data_count = source_context.get_table_count(source_connection.Database.Query)
        return data_count

    def get_source_data(self, data_integration_id: int, paging_modifier: PagingModifier) -> List[any]:
        source_connection = self.data_integration_connection_service.get_source_connection(
            data_integration_id=data_integration_id)
        source_context = self.database_provider.get_context(connection=source_connection.Connection)
        first_row = self.data_integration_column_service.get_first_row(data_integration_id=data_integration_id)
        data = source_context.get_table_data(
            query=source_connection.Database.Query,
            first_row=f'"{first_row.SourceColumnName}"',
            start=paging_modifier.Start,
            end=paging_modifier.End
        )
        return data

    @staticmethod
    def get_paging_modifiers(data_count, limit):
        end = limit
        start = 0
        paging_modifiers = []
        id = 0
        while True:
            if end != limit and end - data_count > limit:
                break
            id = id + 1
            paging_modifier = PagingModifier(Id=id, End=end, Start=start, Limit=limit)
            paging_modifiers.append(paging_modifier)
            end += limit
            start += limit
        return paging_modifiers

    def start_source_data_operation_temp(self,
                                    data_integration_id: int,
                                    data_operation_job_execution_integration_id: int,
                                    limit: int,
                                    process_count: int,
                                    data_queue: Queue,
                                    data_result_queue: Queue):
        source_connection = self.data_integration_connection_service.get_source_connection(
            data_integration_id=data_integration_id)
        source_context = self.database_provider.get_context(connection=source_connection.Connection)
        source_context.get_unpredicted_data(query=source_connection.Database.Query,
                                            columns=None,
                                            limit=limit,
                                            process_count=process_count,
                                            data_queue=data_queue,
                                            result_queue=data_result_queue)

    def read_data(self,
                  data_integration_id: int,
                  limit: int,
                  ):

        source_connection = self.data_integration_connection_service.get_source_connection(
            data_integration_id=data_integration_id)
        source_context = self.database_provider.get_context(connection=source_connection.Connection)
        return source_context.read_data(query=source_connection.Database.Query,
                                        columns=None,
                                        limit=limit)

    def start_source_data_operation(self,
                                        data_integration_id: int,
                                        data_operation_job_execution_integration_id: int,
                                        limit: int,
                                        process_count: int,
                                        data_queue: Queue,
                                        data_result_queue: Queue):

        data_count = self.get_source_data_count(
            data_integration_id=data_integration_id)
        if data_count > 0:
            paging_modifiers = self.get_paging_modifiers(data_count=data_count, limit=limit)
            transmitted_data_count = 0
            for paging_modifier in paging_modifiers:
                # source_data = self.get_source_data(data_integration_id=data_integration_id,
                #                                    paging_modifier=paging_modifier)
                # df = DataFrame(source_data)
                # data = json.loads(df.to_json(orient='records', date_format="iso"))
                # data_types = dict((c, df[c].dtype.name) for c in df.columns)
                # dict((c,df[c].dtype.name) for i in df.columns for j in i.items())
                data_queue_task = DataQueueTask(Id=paging_modifier.Id, Data=None,IsDataFrame=False,
                                                Start=paging_modifier.Start,
                                                End=paging_modifier.End, Limit=limit, IsFinished=False)
                data_queue.put(data_queue_task)
                transmitted_data_count = transmitted_data_count + 1
                if transmitted_data_count >= process_count:
                    result = data_result_queue.get()
                    if result:
                        transmitted_data_count = transmitted_data_count - 1
                    else:
                        break

    def prepare_insert_row(self, data, columns):
        insert_rows = []
        for extracted_data in data:
            row = []
            for column in columns:
                column_data = extracted_data[column]
                row.append(column_data)
            insert_rows.append(tuple(row))
        return insert_rows
    def prepare_data(self, data_integration_id: int, source_data: any) -> List[any]:
        data_integration_columns = self.data_integration_column_service.get_columns_by_integration_id(
            data_integration_id=data_integration_id)

        source_columns = [(data_integration_column.SourceColumnName) for data_integration_column in
                              data_integration_columns]
        prepared_data=self.prepare_insert_row(data=source_data,columns=source_columns)
        # data = source_data[source_column_rows]
        # prepared_data = data.values.tolist()
        return prepared_data

    def prepare_target_query(self, data_integration_id: int) -> str:
        target_connection = self.data_integration_connection_service.get_target_connection(
            data_integration_id=data_integration_id)

        target_context = self.database_provider.get_context(connection=target_connection.Connection)

        data_integration_columns = self.data_integration_column_service.get_columns_by_integration_id(
            data_integration_id=data_integration_id)

        column_rows = [(data_integration_column.ResourceType, data_integration_column.SourceColumnName,
                        data_integration_column.TargetColumnName) for data_integration_column in
                       data_integration_columns]
        prepared_target_query = target_context.prepare_target_query(
            column_rows=column_rows,
            query=target_connection.Database.Query)
        return prepared_target_query

    def write_target_data(self, data_integration_id: int, prepared_data: List[any], ) -> int:
        target_connection = self.data_integration_connection_service.get_target_connection(
            data_integration_id=data_integration_id)

        target_context = self.database_provider.get_context(connection=target_connection.Connection)

        prepared_target_query = self.prepare_target_query(data_integration_id=data_integration_id)
        # rows insert to database
        affected_row_count = target_context.execute_many(query=prepared_target_query, data=prepared_data)
        return affected_row_count

    def do_target_operation(self, data_integration_id: int) -> int:
        target_connection = self.data_integration_connection_service.get_target_connection(
            data_integration_id=data_integration_id)
        target_context = self.database_provider.get_context(connection=target_connection.Connection)

        affected_rowcount = target_context.execute(query=target_connection.Database.Query)

        return affected_rowcount
