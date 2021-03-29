from queue import Queue
from typing import List

from injector import inject
import pandas as pd
from pandas import DataFrame

from domain.integration.services.DataIntegrationColumnService import DataIntegrationColumnService
from domain.integration.services.DataIntegrationConnectionService import DataIntegrationConnectionService
from infrastructor.connection.adapters.ConnectionAdapter import ConnectionAdapter
from infrastructor.connection.queue.QueueProvider import QueueProvider
from infrastructor.exceptions.NotSupportedFeatureException import NotSupportedFeatureException
from models.dto.PagingModifier import PagingModifier


class QueueAdapter(ConnectionAdapter):
    @inject
    def __init__(self,
                 queue_provider: QueueProvider,
                 data_integration_connection_service: DataIntegrationConnectionService,
                 data_integration_column_service: DataIntegrationColumnService,
                 ):
        self.queue_provider = queue_provider
        self.data_integration_column_service = data_integration_column_service
        self.data_integration_connection_service = data_integration_connection_service

    def clear_data(self, data_integration_id) -> int:
        target_connection = self.data_integration_connection_service.get_target_connection(
            data_integration_id=data_integration_id)
        target_context = self.queue_provider.get_context(connection=target_connection.Connection)
        target_context.delete_topic(topic_name=target_connection.Queue.TopicName)
        target_context.create_topic(topic_name=target_connection.Queue.TopicName)
        return 1

    def start_source_data_operation(self,
                                    data_integration_id: int,
                                    data_operation_job_execution_integration_id: int,
                                    limit: int,
                                    process_count: int,
                                    data_queue: Queue,
                                    data_result_queue: Queue):
        source_connection = self.data_integration_connection_service.get_source_connection(
            data_integration_id=data_integration_id)

        source_context = self.queue_provider.get_context(connection=source_connection.Connection)
        source_context.get_unpredicted_data(topic_name=source_connection.Queue.TopicName, group_id="test",
                                            limit=limit,
                                            process_count=process_count,
                                            data_queue=data_queue,
                                            result_queue=data_result_queue)

    def get_source_data_count(self, data_integration_id) -> int:
        return -1

    def get_source_data(self, data_integration_id: int, paging_modifier: PagingModifier) -> DataFrame:
        raise NotSupportedFeatureException("Queue Get Source Data")

    def prepare_data(self, data_integration_id: int, source_data: List[any]) -> List[any]:
        data_integration_columns = self.data_integration_column_service.get_columns_by_integration_id(
            data_integration_id=data_integration_id)

        source_column_rows = [(data_integration_column.SourceColumnName) for data_integration_column in
                              data_integration_columns]
        data = source_data[source_column_rows]
        prepared_data = data.values.tolist()
        return prepared_data

    def write_target_data(self, data_integration_id: int, prepared_data: List[any], ) -> int:
        target_connection = self.data_integration_connection_service.get_target_connection(
            data_integration_id=data_integration_id)

        target_context = self.queue_provider.get_context(connection=target_connection.Connection)
        data_integration_columns = self.data_integration_column_service.get_columns_by_integration_id(
            data_integration_id=data_integration_id)
        columns = [(data_integration_column.TargetColumnName) for data_integration_column in
                   data_integration_columns]
        df = pd.DataFrame(prepared_data, columns=columns)
        data = df.where(pd.notnull(df), None)
        affected_row_count = target_context.write_data(
            topic_name=target_connection.Queue.TopicName, messages=data)
        return affected_row_count

    def do_target_operation(self, data_integration_id: int) -> int:
        raise NotSupportedFeatureException("Queue Target Operation")
