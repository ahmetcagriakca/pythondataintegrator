import json
import os
from unittest import TestCase

from infrastructor.IocManager import IocManager
from tests.integrationtests.common.TestManager import TestManager


class TestConnectorTypeResource(TestCase):

    def __init__(self, methodName='TestConnectorTypeResource'):
        super(TestConnectorTypeResource, self).__init__(methodName)
        self.test_manager = TestManager()

    def print_error_detail(self, data):
        print(data['message'] if 'message' in data else '')
        print(data['traceback'] if 'traceback' in data else '')
        print(data['message'] if 'message' in data else '')

    def test_get_connector_type(self):
        response_data = self.test_manager.service_endpoints.get_connector_type()
        assert response_data['IsSuccess'] == True
