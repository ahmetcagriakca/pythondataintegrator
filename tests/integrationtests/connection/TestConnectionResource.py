import json
import os
from unittest import TestCase

from infrastructor.IocManager import IocManager
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from models.dao.connection.Connection import Connection
from models.dao.connection.ConnectionDatabase import ConnectionDatabase
from tests.integrationtests.common.TestManager import TestManager


class TestConnectionResuource(TestCase):
    def __init__(self, methodName='TestConnectionResuource'):
        super(TestConnectionResuource, self).__init__(methodName)
        self.test_manager = TestManager()

    def test_get_connection(self):
        response_data = self.test_manager.service_endpoints.get_connection()
        assert response_data['IsSuccess'] == True


    def test_delete_connection(self):
        id = 1
        test_data = {"Id": id}
        try:
            response_data = self.test_manager.service_endpoints.delete_connection(test_data)
            assert response_data["Message"] == "Connection Removed Successfully"
        except Exception as ex:
            assert True == False
        finally:
            # clean data_integration test operations
            database_session_manager: DatabaseSessionManager = self.test_manager.ioc_manager.injector.get(
                DatabaseSessionManager)
            connection_database_repository: Repository[ConnectionDatabase] = Repository[ConnectionDatabase](
                database_session_manager)
            connection_repository: Repository[Connection] = Repository[Connection](
                database_session_manager)
            connection = connection_repository.first(Id=id)
            connection_database = connection_database_repository.first(Connection=connection)
            connection.IsDeleted = 0
            connection_database.IsDeleted = 0
            database_session_manager.commit()
