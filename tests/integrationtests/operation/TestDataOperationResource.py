from unittest import TestCase

from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
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
        self.test_manager.service_scenarios.create_test_connection(DataOperationTestData.test_integration_connection)
        self.test_manager.service_scenarios.create_test_integration(
            DataOperationTestData.test_data_operation_integration_input)
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
            self.test_manager.service_scenarios.clear_operation(name=DataOperationTestData.test_insert_input['Name'])
