from infrastructor.IocManager import IocManager
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from models.dao.connection.Connection import Connection
from models.dao.integration.DataIntegration import DataIntegration
from tests.integrationtests.common.TestServiceEndpoints import TestServiceEndpoints


class TestServiceScenarios:
    def __init__(self,
                 service_endpoints: TestServiceEndpoints,
                 ioc_manager: IocManager):
        self.ioc_manager = ioc_manager
        self.service_endpoints = service_endpoints

    def create_test_connection(self, test_integration_connection):
        database_session_manager: DatabaseSessionManager = self.ioc_manager.injector.get(
            DatabaseSessionManager)
        connection_repository: Repository[Connection] = Repository[Connection](
            database_session_manager)

        connection = connection_repository.first(Name=test_integration_connection["Name"])
        if connection is None:
            response_data = self.service_endpoints.insert_connection_database(test_integration_connection)

    def create_test_integration(self, test_data_operation_integration):
        database_session_manager: DatabaseSessionManager = self.ioc_manager.injector.get(
            DatabaseSessionManager)
        data_integration_repository: Repository[DataIntegration] = Repository[DataIntegration](
            database_session_manager)
        data_integration = data_integration_repository.first(Code=test_data_operation_integration["Code"])
        if data_integration is None:
            response_data = self.service_endpoints.insert_data_integration(test_data_operation_integration)
