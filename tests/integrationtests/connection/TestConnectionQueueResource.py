from unittest import TestCase

from domain.connection.services.ConnectionSecretService import ConnectionSecretService
from infrastructor.IocManager import IocManager
from tests.integrationtests.common.TestManager import TestManager
from tests.integrationtests.connection.testdata.TestConnectionQueueData import TestConnectionQueueData


class TestConnectionQueueResource(TestCase):
    def __init__(self, methodName='TestConnectionQueueResource'):
        super(TestConnectionQueueResource, self).__init__(methodName)
        self.test_manager = TestManager()

    def test_connection(self):
        expected = True
        connection_secret_service = IocManager.injector.get(ConnectionSecretService)
        try:
            response_data = self.test_manager.service_endpoints.create_connection_queue(
                TestConnectionQueueData.test_insert_input)
            assert response_data['IsSuccess'] == expected
            assert response_data['Result']['Name'] == TestConnectionQueueData.test_insert_input['Name']
            basic_authentication = connection_secret_service.get_connection_basic_authentication(
                connection_id=response_data['Result']['Id'])
            assert basic_authentication.User == TestConnectionQueueData.test_insert_input['User']
            assert basic_authentication.Password == TestConnectionQueueData.test_insert_input['Password']
            response_data = self.test_manager.service_endpoints.create_connection_queue(
                TestConnectionQueueData.test_update_input)
            assert response_data['IsSuccess'] == expected
            assert response_data['Result']['Queue']['ConnectorType']['Name'] == \
                   TestConnectionQueueData.test_update_input["ConnectorTypeName"]

            delete_request = {
                "Id": response_data['Result']['Id']
            }
            response_data = self.test_manager.service_endpoints.delete_connection(delete_request)
            assert response_data['IsSuccess'] == expected

        except Exception as ex:
            assert True == False
        finally:
            # clean
            pass
            self.test_manager.service_scenarios.clear_connection(TestConnectionQueueData.test_insert_input['Name'])
