from pdip.data import RepositoryProvider
from pdip.dependency.container import DependencyContainer
from pdip.logging.loggers.database import SqlLogger

from pdip.data import Seed
from pdi.domain.connection import ConnectionType, ConnectorType


class ConnectionSeed(Seed):
    def seed(self):
        try:
            repository_provider = DependencyContainer.Instance.get(RepositoryProvider)
            connection_type_repository = repository_provider.get(ConnectionType)
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
                    }
                ]
                for connection_type_json in connection_type_list:
                    connection_type = ConnectionType(Name=connection_type_json["Name"])
                    connection_type_repository.insert(connection_type)
                    repository_provider.commit()

            connector_type_repository = repository_provider.get(ConnectorType)
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
                    }
                ]
                for connector_type_json in connector_type_list:
                    connection_type = connection_type_repository.filter_by(
                        Name=connector_type_json["ConnectionType"]).first()
                    connector_type = ConnectorType(Name=connector_type_json["Name"],
                                                   ConnectionType=connection_type)
                    connector_type_repository.insert(connector_type)
                    repository_provider.commit()
        except Exception as ex:
            logger = DependencyContainer.Instance.get(SqlLogger)
            logger.exception(ex, "ApScheduler seeds getting error")
        finally:
            repository_provider.close()
