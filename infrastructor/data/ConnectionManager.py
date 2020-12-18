import time
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
    def fetch(self, query):
        cur = self.connector.connection.cursor()
        cur.execute(query)
        datas = cur.fetchall()
        data_list = []
        for data in datas:
            rows = []
            for row in data:
                rows.append(row)
            data_list.append(rows)
        return data_list

    @connect
    def insert(self, query) -> None:
        return self.cursor.execute(query)

    @connect
    def delete(self, query) -> None:
        cur = self.connector.connection.cursor()
        cur.execute(query)
        self.connector.connection.commit()
    
    @connect
    def run_query(self, query) -> None:
        cur = self.connector.connection.cursor()
        cur.execute(query)
        self.connector.connection.commit()

    @connect
    def insert_many(self, executable_script, data):
        return self._insert_to_db_with_retry(executable_script, data, self.default_retry)

    def _insert_many_start(self, executable_script, data):
        cur = self.connector.connection.cursor()
        cur.executemany(executable_script, data)
        self.connector.connection.commit()

    def _insert_to_db_with_retry(self, executable_script, data, retry):
        try:
            self._insert_many_start(executable_script, data)
        except Exception as ex:
            if retry > self.retry_count:
                self.sql_logger.error(f"Db write error on Error:{ex}")
                return False
            self.sql_logger.error(
                f"Getting error on insert (Operation will be retried. Retry Count:{retry}). Error:{ex}")
            # retrying connect to db,
            self.connector.connect()
            time.sleep(1)
            return self._insert_to_db_with_retry(executable_script, data, retry + 1)
        return True
