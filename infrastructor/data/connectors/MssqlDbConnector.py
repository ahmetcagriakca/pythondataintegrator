import pyodbc
from infrastructor.data.ConnectorStrategy import ConnectorStrategy
from models.configs.DatabaseConfig import DatabaseConfig


class MssqlDbConnector(ConnectorStrategy):
    def __init__(self, database_config: DatabaseConfig):
        self.database_config: DatabaseConfig = database_config
        if self.database_config.driver is None or self.database_config.driver == "":
            self.database_config.driver = 'ODBC Driver 17 for SQL Server'
        self.connection_string = 'DRIVER={%s};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (
            self.database_config.driver, self.database_config.host, self.database_config.database,
            self.database_config.username, self.database_config.password)

        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = pyodbc.connect(self.connection_string)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        try:
            if self.cursor is not None:
                self.cursor.close()

            if self.connection is not None:
                self.connection.close()
        except Exception:
            pass

    def execute_many(self,query,data):
        cursor = self.connection.cursor()
        cursor.fast_executemany = True
        try:
            cursor.executemany(query, data)
            self.connection.commit()
        except Exception as error:
            self.connection.rollback()
            cursor.close()
            raise error