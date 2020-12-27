import json
import os
from unittest import TestCase

from infrastructor.IocManager import IocManager
from tests.integrationtests.common.TestManager import TestManager


class TestConnectionTypeResuource(TestCase):

    def __init__(self, methodName='TestConnectionTypeResuource'):
        super(TestConnectionTypeResuource, self).__init__(methodName)
        self.test_manager = TestManager()

    def test_get_connection_type(self):
        response_data = self.test_manager.service_endpoints.get_connection_type()
        assert response_data['IsSuccess'] == True
