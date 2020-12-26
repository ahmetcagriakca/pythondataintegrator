import psycopg2
from injector import inject
from infrastructor.data.ConnectorStrategy import ConnectorStrategy
from models.configs.DatabaseConfig import DatabaseConfig
import psycopg2.extras as extras


class PostgreDbConnector(ConnectorStrategy):
    @inject
    def __init__(self, database_config: DatabaseConfig):
        self.database_config = database_config
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = psycopg2.connect(user=self.database_config.username, password=self.database_config.password,
                                           database=self.database_config.database, host=self.database_config.host,
                                           port=self.database_config.port)
        self.cursor = self.connection.cursor()

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
            extras.execute_batch(self.cursor, query, data, 10000)
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.cursor.close()
            raise error
