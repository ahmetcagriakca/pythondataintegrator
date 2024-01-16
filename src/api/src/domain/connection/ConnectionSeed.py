from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.data.seed import Seed
from pdip.logging.loggers.sql import SqlLogger

from src.domain.connection import ConnectionType, ConnectorType


class ConnectionSeed(Seed):
    @inject
    def __init__(
            self,
            repository_provider: RepositoryProvider,
            logger: SqlLogger,
    ):
        self.logger = logger
        self.repository_provider = repository_provider

    def seed(self):
        try:
            connection_type_repository = self.repository_provider.get(ConnectionType)
            check_count = connection_type_repository.table.count()
            if check_count is None or check_count == 0:

                connection_type_list = [
                    {
                        "Name": "Database",
                    },
                    {
                        "Name": "File",
                    },
                    {
                        "Name": "Queue",
                    },
                    {
                        "Name": "BigData",
                    }
                ]
                for connection_type_json in connection_type_list:
                    connection_type = ConnectionType(Name=connection_type_json["Name"])
                    connection_type_repository.insert(connection_type)
                    self.repository_provider.commit()

            connector_type_repository = self.repository_provider.get(ConnectorType)
            check_count = connector_type_repository.table.count()
            if check_count is None or check_count == 0:
                connector_type_list = [
                    {
                        "ConnectionType": "Database",
                        "Name": "MSSQL",
                    },
                    {
                        "ConnectionType": "Database",
                        "Name": "ORACLE",
                    },
                    {
                        "ConnectionType": "Database",
                        "Name": "POSTGRESQL",
                    },
                    {
                        "ConnectionType": "File",
                        "Name": "EXCEL",
                    },
                    {
                        "ConnectionType": "File",
                        "Name": "CSV",
                    },
                    {
                        "ConnectionType": "Queue",
                        "Name": "Kafka",
                    },
                    {
                        "ConnectionType": "Database",
                        "Name": "MYSQL",
                    },
                    {
                        "ConnectionType": "Database",
                        "Name": "Impala",
                    },
                    {
                        "ConnectionType": "Database",
                        "Name": "CLICKHOUSE",
                    },
                ]
                for connector_type_json in connector_type_list:
                    connection_type = connection_type_repository.filter_by(
                        Name=connector_type_json["ConnectionType"]).first()
                    connector_type = ConnectorType(Name=connector_type_json["Name"],
                                                   ConnectionType=connection_type)
                    connector_type_repository.insert(connector_type)
                    self.repository_provider.commit()
        except Exception as ex:
            self.logger.exception(ex, "ApScheduler seeds getting error")
