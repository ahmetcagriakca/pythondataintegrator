import json
import os
from unittest import TestCase

import pytest

from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from models.dao.connection.Connection import Connection
from models.dao.connection.ConnectionDatabase import ConnectionDatabase
from tests.integrationtests.common.TestManager import TestManager
from tests.integrationtests.connection.testdata.ConnectionTestData import ConnectionTestData


class TestConnectionDatabaseResuource(TestCase):
    def __init__(self, methodName='TestConnectionDatabaseResuource'):
        super(TestConnectionDatabaseResuource, self).__init__(methodName)
        self.test_manager = TestManager()

    def test_database_connection(self):
        expected = True
        try:
            response_data = self.test_manager.service_endpoints.insert_connection_database(
                ConnectionTestData.test_insert_input)
            assert response_data['IsSuccess'] == expected
            assert response_data['Result']['Name'] == ConnectionTestData.test_insert_input['Name']
            response_data = self.test_manager.service_endpoints.update_connection_database(
                ConnectionTestData.test_update_input)
            assert response_data['IsSuccess'] == expected
            assert response_data['Result']['Database']['ConnectorType']['Name'] == \
                   ConnectionTestData.test_update_input["ConnectorTypeName"]
        except Exception as ex:
            assert True == False
        finally:
            # clean integration test operations
            self.test_manager.service_scenarios.clear_connection(ConnectionTestData.test_insert_input['Name'])
