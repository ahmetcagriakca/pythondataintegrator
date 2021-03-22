from injector import inject
from pandas import DataFrame

from infrastructor.connection.queue.connectors.QueueConnector import QueueConnector
from infrastructor.dependency.scopes import IScoped


class QueueContext(IScoped):
    @inject
    def __init__(self,
                 connector: QueueConnector
                 ):
        self.connector: QueueConnector = connector

    def create_topic(self, topic_name):
        return self.connector.create_topic(topic_name=topic_name)

    def delete_topic(self, topic_name):
        return self.connector.delete_topic(topic_name=topic_name)

    def write_data(self, topic_name: str, messages: DataFrame):
        return self.connector.write_data(topic_name=topic_name, messages=messages)

    def get_data(self, topic_name: str, group_id: str, limit: int, auto_offset_reset: str = 'earliest',
                 enable_auto_commit: bool = True):
        self.connector.create_consumer(topic_name=topic_name, group_id=group_id, auto_offset_reset=auto_offset_reset,
                                       enable_auto_commit=enable_auto_commit)
        data = self.connector.get_data(limit=limit)
        return data

    def prepare_insert_row(self, data, column_rows):
        insert_rows = []
        for extracted_data in data:
            row = []
            for column_row in column_rows:
                prepared_data = extracted_data[column_rows.index(column_row)]
                row.append(prepared_data)
            insert_rows.append(tuple(row))
        return insert_rows