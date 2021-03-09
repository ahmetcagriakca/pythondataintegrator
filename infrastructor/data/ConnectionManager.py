import time
import re

from injector import inject
from infrastructor.data.ConnectionPolicy import ConnectionPolicy
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger


class ConnectionManager(IScoped):
    @inject
    def __init__(self, connection_policy: ConnectionPolicy, sql_logger: SqlLogger, retry_count=3):
        self.sql_logger: SqlLogger = sql_logger
        self.connector = connection_policy.connector
        self.retry_count = retry_count
        self.default_retry = 1

    def connect(func):
        def inner(*args, **kwargs):
            try:
                args[0].connector.connect()
                return func(*args, **kwargs)
            finally:
                args[0].connector.disconnect()

        return inner

    @connect
    def fetch_query(self, query):
        self.connector.cursor.execute(query)
        datas = self.connector.cursor.fetchall()
        return datas

    def fetch(self, query):
        datas = self.fetch_query(query=query)
        data_list = []
        for data in datas:
            rows = []
            for row in data:
                rows.append(row)
            data_list.append(rows)
        return data_list

    @connect
    def execute(self, query) -> any:
        self.connector.cursor.execute(query)
        self.connector.connection.commit()
        return self.connector.cursor.rowcount

    @connect
    def execute_many(self, query, data):
        return self._execute_with_retry(query=query, data=data, retry=self.default_retry)

    def _execute_many_start(self, query, data):
        self.connector.execute_many(query=query, data=data)

    def _execute_with_retry(self, query, data, retry):
        try:
            self._execute_many_start(query=query, data=data)
        except Exception as ex:
            if retry > self.retry_count:
                self.sql_logger.error(f"Db write error on Error:{ex}")
                raise
            self.sql_logger.error(
                f"Getting error on insert (Operation will be retried. Retry Count:{retry}). Error:{ex}")
            # retrying connect to db,
            self.connector.connect()
            time.sleep(1)
            return self._execute_with_retry(query=query, data=data, retry=retry + 1)
        return True

    def get_table_count(self, query):
        count_query = self.connector.get_table_count_query(query=query)
        datas = self.fetch_query(query=count_query)
        return datas[0][0]

    def get_table_data(self, query, first_row, sub_limit, top_limit):
        data_query = self.connector.get_table_data_query(query=query, first_row=first_row, sub_limit=sub_limit,
                                                         top_limit=top_limit)
        return self.fetch(data_query)

    def truncate_table(self, schema, table):
        truncate_query = self.connector.get_truncate_query(schema=schema, table=table)
        return self.execute(query=truncate_query)

    def replace_regex(self, text, field, indexer):
        text = re.sub(r'\(:' + field + r'\b', f'({indexer}', text)
        text = re.sub(r':' + field + r'\b\)', f'{indexer})', text)
        text = re.sub(r':' + field + r'\b', f'{indexer}', text)
        return text

    def prepare_target_query(self, column_rows, query):
        target_query = query
        for column_row in column_rows:
            index = column_rows.index(column_row)
            indexer = self.connector.get_target_query_indexer().format(index=index)
            target_query = self.replace_regex(target_query, column_row[1], indexer)
        return target_query

    def prepare_insert_row(self, extracted_datas, column_rows):
        insert_rows = []
        for extracted_data in extracted_datas:
            row = []
            for column_row in column_rows:
                data = self.connector.prepare_data(extracted_data[column_rows.index(column_row)])
                row.append(data)
            insert_rows.append(tuple(row))
        return insert_rows
