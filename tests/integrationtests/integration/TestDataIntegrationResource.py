import json
import os
from unittest import TestCase

from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from models.dao.connection.Connection import Connection
from models.dao.connection.ConnectionDatabase import ConnectionDatabase
from models.dao.integration.DataIntegration import DataIntegration
from models.dao.integration.DataIntegrationColumn import DataIntegrationColumn
from models.dao.integration.DataIntegrationConnection import DataIntegrationConnection
from tests.integrationtests.common.TestManager import TestManager
from tests.integrationtests.connection.testdata.ConnectionTestData import ConnectionTestData
from tests.integrationtests.integration.testdata.DataIntegrationTestData import DataIntegrationTestData


class TestDataIntegrationResuource(TestCase):
    def __init__(self, methodName='TestDataIntegrationResuource'):
        super(TestDataIntegrationResuource, self).__init__(methodName)
        self.test_manager = TestManager()

    def test_get_data_integration(self):
        response_data = self.test_manager.service_endpoints.get_data_integration()
        assert response_data['IsSuccess'] == True

    def test_data_integration(self):

        expected = True
        expected_insert_source_query = f'SELECT "Id", "Name" FROM "test"."test_integration_source"'
        expected_insert_target_query = f'INSERT INTO "test"."test_integration_source"("Id", "Name") VALUES (:Id, :Name)'
        expected_update_source_query = f'SELECT "Id", "Name", "Order" FROM "test"."test_integration_source"'
        expected_update_target_query = f'INSERT INTO "test"."test_integration_source"("Id", "Name", "Order") VALUES (:Id, :Name, :Order)'
        self.test_manager.service_scenarios.create_test_connection(ConnectionTestData.test_integration_connection)
        try:
            response_data = self.test_manager.service_endpoints.insert_data_integration(DataIntegrationTestData.test_insert_input)
            assert response_data['IsSuccess'] == expected
            assert response_data['Result']['Code'] == DataIntegrationTestData.test_insert_input['Code']
            assert response_data['Result']['SourceConnection']['Query'] == expected_insert_source_query
            assert response_data['Result']['TargetConnection']['Query'] == expected_insert_target_query

            response_data = self.test_manager.service_endpoints.update_data_integration(DataIntegrationTestData.test_update_input)
            assert response_data['IsSuccess'] == expected
            assert response_data['Result']['Code'] == DataIntegrationTestData.test_insert_input['Code']
            assert response_data['Result']['SourceConnection']['Query'] == expected_update_source_query
            assert response_data['Result']['TargetConnection']['Query'] == expected_update_target_query
            delete_request = {"Code": DataIntegrationTestData.test_insert_input["Code"]}
            response_data = self.test_manager.service_endpoints.delete_data_integration(delete_request)
            assert response_data['Message'] == f'Data integration deletion for {delete_request["Code"]} is Completed'
        except Exception as ex:
            assert True == False
        finally:
            # clean integration test operations
            database_session_manager: DatabaseSessionManager = self.test_manager.ioc_manager.injector.get(
                DatabaseSessionManager)
            data_integration_repository: Repository[DataIntegration] = Repository[DataIntegration](
                database_session_manager)
            data_integration = data_integration_repository.first(Code=DataIntegrationTestData.test_insert_input['Code'])

            for data_integration_column in data_integration.Columns:
                database_session_manager.session.delete(data_integration_column)
            for data_integration_execution_job in data_integration.ExecutionJobs:
                database_session_manager.session.delete(data_integration_execution_job)
            for data_integration_connection in data_integration.Connections:
                database_session_manager.session.delete(data_integration_connection)

            database_session_manager.session.delete(data_integration)
            database_session_manager.commit()
