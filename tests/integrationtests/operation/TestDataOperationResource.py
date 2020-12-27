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
from models.dao.operation import DataOperation
from tests.integrationtests.common.TestManager import TestManager
from tests.integrationtests.connection.testdata.ConnectionTestData import ConnectionTestData
from tests.integrationtests.integration.testdata.DataIntegrationTestData import DataIntegrationTestData
from tests.integrationtests.operation.testdata.DataOperationTestData import DataOperationTestData


class TestDataOperationResource(TestCase):
    def __init__(self, methodName='TestDataOperationResource'):
        super(TestDataOperationResource, self).__init__(methodName)
        self.test_manager = TestManager()

    def test_data_integration(self):
        expected = True
        self.test_manager.service_scenarios.create_test_connection(ConnectionTestData.test_integration_connection)
        self.test_manager.service_scenarios.create_test_integration(
            DataIntegrationTestData.test_data_operation_integration_input)
        try:
            response_data = self.test_manager.service_endpoints.insert_data_operation(
                DataOperationTestData.test_insert_input)
            assert response_data['IsSuccess'] == expected
            assert response_data['Result']['Name'] == DataOperationTestData.test_insert_input['Name']
            assert response_data['Result']['Integrations'][0]["Integration"]["Code"] == \
                   DataOperationTestData.test_insert_input['Integrations'][0]["Code"]

            response_data = self.test_manager.service_endpoints.update_data_operation(
                DataOperationTestData.test_update_input)
            assert response_data['IsSuccess'] == expected
            assert response_data['Result']['Name'] == DataOperationTestData.test_insert_input['Name']
            assert response_data['Result']['Integrations'][0]["Limit"] == \
                   DataOperationTestData.test_update_input['Integrations'][0]["Limit"]
            assert response_data['Result']['Integrations'][0]["ProcessCount"] == \
                   DataOperationTestData.test_update_input['Integrations'][0]["ProcessCount"]

            delete_request = {"Id": response_data["Result"]["Id"]}
            response_data = self.test_manager.service_endpoints.delete_data_operation(delete_request)
            assert response_data['Message'] == f'Data Operation removed successfully'
        except Exception as ex:
            assert True == False
        finally:
            # clean integration test operations
            database_session_manager: DatabaseSessionManager = self.test_manager.ioc_manager.injector.get(
                DatabaseSessionManager)
            data_integration_repository: Repository[DataOperation] = Repository[DataOperation](
                database_session_manager)
            data_operation = data_integration_repository.first(Name=DataOperationTestData.test_insert_input['Name'])

            for data_operation_integration in data_operation.Integrations:
                database_session_manager.session.delete(data_operation_integration)
            for data_operation_job in data_operation.DataOperationJobs:
                database_session_manager.session.delete(data_operation_job)

            database_session_manager.session.delete(data_operation)
            database_session_manager.commit()
