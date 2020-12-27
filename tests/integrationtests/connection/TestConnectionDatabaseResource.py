import json
import os
from unittest import TestCase

import pytest

from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from models.dao.connection.Connection import Connection
from models.dao.connection.ConnectionDatabase import ConnectionDatabase
from tests.integrationtests.common.TestManager import TestManager
from tests.integrationtests.connection.testdata.connection_test_data import ConnectionTestData


class TestConnectionDatabaseResuource(TestCase):
    def __init__(self, methodName='TestConnectionDatabaseResuource'):
        super(TestConnectionDatabaseResuource, self).__init__(methodName)
        self.test_manager = TestManager()

    def insert_connection(self, request):
        # insert connection
        response_data = self.test_manager.api_client.post('/api/Connection/ConnectionDatabase', request)
        return response_data

    def update_connection(self, request):
        # update connection
        response_data = self.test_manager.api_client.put('/api/Connection/ConnectionDatabase', request)
        return response_data

    def test_database_connection(self):
        expected = True
        try:
            response_data = self.insert_connection(ConnectionTestData.test_insert_input)
            assert response_data['IsSuccess'] == expected
            assert response_data['Result']['Name'] == ConnectionTestData.test_insert_input['Name']
            response_data = self.update_connection(ConnectionTestData.test_update_input)
            assert response_data['IsSuccess'] == expected
            assert response_data['Result']['Database'][0]['ConnectorType'][0]['Name'] == \
                   ConnectionTestData.test_update_input["ConnectorTypeName"]
        except Exception as ex:
            assert True == False
        finally:
            # clean integration test operations
            database_session_manager: DatabaseSessionManager = self.test_manager.ioc_manager.injector.get(DatabaseSessionManager)

            connection_database_repository: Repository[ConnectionDatabase] = Repository[ConnectionDatabase](
                database_session_manager)
            connection_repository: Repository[Connection] = Repository[Connection](
                database_session_manager)
            connection = connection_repository.first(Name=ConnectionTestData.test_insert_input['Name'], IsDeleted=0)
            connection_database = connection_database_repository.first(Connection=connection, IsDeleted=0)
            database_session_manager.session.delete(connection_database)
            database_session_manager.session.delete(connection)
            database_session_manager.commit()
