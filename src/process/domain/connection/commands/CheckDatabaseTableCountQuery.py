from IocManager import IocManager
from domain.operation.execution.services.OperationCacheService import OperationCacheService
from infrastructure.connection.database.DatabaseProvider import DatabaseProvider
from infrastructure.cryptography.CryptoService import CryptoService
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.logging.SqlLogger import SqlLogger
from models.configs.ApplicationConfig import ApplicationConfig
from models.dao.connection import Connection


class CheckDatabaseTableCountQuery:
    def execute(self, connection_name=None, schema=None, table=None):
        try:
            repository_provider: RepositoryProvider = RepositoryProvider()

            connection = repository_provider.get(Connection).first(IsDeleted=0, Name=connection_name)
            if connection is None:
                return "Connection not found!"
            sql_logger = SqlLogger()
            application_config = IocManager.config_manager.get(ApplicationConfig)
            crypto_service = CryptoService(application_config=application_config)
            operation_cache_service = OperationCacheService(repository_provider=repository_provider,
                                                           crypto_service=crypto_service)
            operation_cache_service.initialize_connection(connection.Id)
            database_provider = DatabaseProvider(sql_logger=sql_logger, operation_cache_service=operation_cache_service)
            database_context = database_provider.get_context(connection=connection)
            database_context.connector.connect()
            count_of_table = ''
            if schema is not None and schema != '' and table is not None and table != '':
                try:
                    count = database_context.get_table_count(f'select * from "{schema}"."{table}"')
                    count_of_table = f'"{schema}"."{table}" table count:{count}'
                except Exception as ex:
                    raise Exception(f'"{schema}"."{table}" count of table getting error! Error: {ex}')
            return count_of_table

        except Exception as ex:
            raise Exception(f'Connection getting error! Error: {ex}')
