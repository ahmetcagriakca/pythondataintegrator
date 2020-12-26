import cx_Oracle
from injector import inject
from infrastructor.data.ConnectorStrategy import ConnectorStrategy
from models.configs.DatabaseConfig import DatabaseConfig


class OracleDbConnector(ConnectorStrategy):
    @inject
    def __init__(self, database_config: DatabaseConfig):
        self.database_config = database_config
        self._tns = cx_Oracle.makedsn(self.database_config.host, self.database_config.port,
                                      service_name=self.database_config.database)
        self.connection_string = None
        self.connection = None
        self.cursor = None

    def connect(self):
        if self.database_config.connection_string is not None:
            self.connection = cx_Oracle.connect(self.database_config.connection_string)
        else:
            self.connection = cx_Oracle.connect(self.database_config.username, self.database_config.password, self._tns,
                                                encoding="UTF-8",
                                                nencoding="UTF-8")

    def disconnect(self):
        try:
            if self.cursor is not None:
                self.cursor.close()

            if self.connection is not None:
                self.connection.close()
        except Exception:
            pass

    def execute_many(self, query, data):
        try:
            self.cursor.executemany(query, data)
            self.connection.commit()
        except Exception as error:
            self.connection.rollback()
            self.cursor.close()
            raise error
