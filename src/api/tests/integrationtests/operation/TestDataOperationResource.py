from unittest import TestCase

from domain.operation.services.DataOperationService import DataOperationService
from IocManager import IocManager
from tests.integrationtests.common.TestManager import TestManager
from tests.integrationtests.operation.testdata import TestDataOperationDatabaseData


class TestDataOperationResource(TestCase):
    def __init__(self, methodName='TestDataOperationResource'):
        super(TestDataOperationResource, self).__init__(methodName)
        self.test_manager = TestManager()

    def test_data_operation(self):
        expected = True
        self.test_manager.service_scenarios.create_test_connection_database(TestDataOperationDatabaseData.test_integration_connection)
        try:
            response_data = self.test_manager.service_endpoints.insert_data_operation(
                TestDataOperationDatabaseData.test_insert_input)
            assert response_data['IsSuccess'] == expected
            assert response_data['Result']['Name'] == TestDataOperationDatabaseData.test_insert_input['Name']
            assert response_data['Result']['Integrations'][0]["Integration"]["Code"] == \
                   TestDataOperationDatabaseData.test_insert_input['Integrations'][0]["Integration"]["Code"]
            assert response_data['Result']['Contacts'][0]["Email"] == \
                   TestDataOperationDatabaseData.test_insert_input['Contacts'][0]["Email"]

            response_data = self.test_manager.service_endpoints.insert_data_operation(
                TestDataOperationDatabaseData.test_update_input)
            assert response_data['IsSuccess'] == expected
            assert response_data['Result']['Name'] == TestDataOperationDatabaseData.test_update_input['Name']
            assert response_data['Result']['Integrations'][0]["Limit"] == \
                   TestDataOperationDatabaseData.test_update_input['Integrations'][0]["Limit"]
            assert response_data['Result']['Integrations'][0]["ProcessCount"] == \
                   TestDataOperationDatabaseData.test_update_input['Integrations'][0]["ProcessCount"]
            assert response_data['Result']['Contacts'][0]["Email"] == \
                   TestDataOperationDatabaseData.test_update_input['Contacts'][0]["Email"]
            data_operation = self.test_manager.service_scenarios.get_data_operation(
                name=TestDataOperationDatabaseData.test_insert_input['Name'])
            data_operation.Integrations[0].DataIntegration.Connections
            delete_request = {"Id": data_operation.Id}
            response_data = self.test_manager.service_endpoints.delete_data_operation(delete_request)
            assert response_data['Message'] == f'Data Operation removed successfully'

        except Exception as ex:
            assert True == False
        finally:
            # clean data_integration test operations
            pass
            data_operation = self.test_manager.service_scenarios.get_data_operation(
                name=TestDataOperationDatabaseData.test_insert_input['Name'])
            if data_operation is not None:
                data_operation.Integrations[0].DataIntegration.Connections
                delete_request = {"Id": data_operation.Id}
                response_data = self.test_manager.service_endpoints.delete_data_operation(delete_request)
                assert response_data['Message'] == f'Data Operation removed successfully'
            #self.test_manager.service_scenarios.clear_operation(name=TestDataOperationDatabaseData.test_insert_input['Name'])

    def test_data_operation_same_integration(self):
        expected = True
        self.test_manager.service_scenarios.create_test_connection_database(TestDataOperationDatabaseData.test_integration_connection)
        response_data = self.test_manager.service_endpoints.insert_data_operation(
            TestDataOperationDatabaseData.test_insert_input_same_integration_1)
        assert response_data['IsSuccess'] == expected

        data_operation_service = IocManager.injector.get(DataOperationService)
        data_operation = data_operation_service.get_by_name(
            TestDataOperationDatabaseData.test_insert_input_same_integration_1["Name"])
        assert len(data_operation.Integrations) == 1
        assert data_operation.Integrations[0].DataIntegration.Code == \
               TestDataOperationDatabaseData.test_insert_input_same_integration_1['Integrations'][0]["Integration"]["Code"]
        assert data_operation.Integrations[0].DataIntegration.Code == \
               response_data['Result']['Integrations'][0]["Integration"]["Code"]
        response_data = self.test_manager.service_endpoints.insert_data_operation(
            TestDataOperationDatabaseData.test_insert_input_same_integration_2)
        assert response_data['IsSuccess'] == expected
        assert len(data_operation.Integrations) == 1
        assert data_operation.Integrations[0].DataIntegration.Code == \
               TestDataOperationDatabaseData.test_insert_input_same_integration_2['Integrations'][0]["Integration"]["Code"]
        assert data_operation.Integrations[0].DataIntegration.Code == \
               response_data['Result']['Integrations'][0]["Integration"]["Code"]
