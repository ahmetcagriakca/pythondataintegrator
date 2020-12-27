import json
import os
from unittest import TestCase

import pytest

from infrastructor.IocManager import IocManager
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from models.dao.connection.Connection import Connection
from models.dao.connection.ConnectionDatabase import ConnectionDatabase


class TestConnectionDatabaseResuource(TestCase):
    def __init__(self, methodName='TestConnectionDatabaseResuource'):
        super(TestConnectionDatabaseResuource, self).__init__(methodName)

        from infrastructor.api.FlaskAppWrapper import FlaskAppWrapper
        from infrastructor.scheduler.JobScheduler import JobScheduler
        os.environ["PYTHON_ENVIRONMENT"] = 'test'
        root_directory = os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, os.pardir))
        IocManager.configure_startup(root_directory=root_directory,
                                     app_wrapper=FlaskAppWrapper,
                                     job_scheduler=JobScheduler)
        self.client = IocManager.app.test_client()

    def print_error_detail(self, data):
        print(data['message'] if 'message' in data else '')
        print(data['traceback'] if 'traceback' in data else '')
        print(data['message'] if 'message' in data else '')

    def insert_connection(self, request, expected):
        # insert connection
        data = json.dumps(request)
        response = self.client.post(
            '/api/Connection/ConnectionDatabase',
            data=data,
            content_type='application/json',
        )
        response_data = json.loads(response.get_data(as_text=True))
        print(response_data)
        assert response.status_code == 200
        self.print_error_detail(response_data)
        assert response_data['IsSuccess'] == expected

    def update_connection(self, request, expected):
        data = json.dumps(request)
        response = self.client.put(
            '/api/Connection/ConnectionDatabase',
            data=data,
            content_type='application/json',
        )
        response_data = json.loads(response.get_data(as_text=True))
        print(response_data)
        assert response.status_code == 200
        self.print_error_detail(response_data)
        assert response_data['IsSuccess'] == expected

    def test_database_connection(self):
        name = 'NewDatabaseConnection'
        test_insert_input = {
            "Name": "NewDatabaseConnection",
            "ConnectionTypeName": "Database",
            "ConnectorTypeName": "POSTGRESQL",
            "Host": "string",
            "Port": 0,
            "Sid": "string",
            "DatabaseName": "string",
            "User": "string",
            "Password": "string"
        }
        test_update_input = {
            "Name": "NewDatabaseConnection",
            "ConnectorTypeName": "MSSQL",
            "Host": "Test",
            "Port": 1550,
            "Sid": "test",
            "DatabaseName": "test",
            "User": "test",
            "Password": "test"
        }
        expected = True
        try:
            self.insert_connection(test_insert_input, expected)
            self.update_connection(test_update_input, expected)
        except Exception as ex:
            assert True == False
        finally:

            # remove new record
            database_session_manager: DatabaseSessionManager = IocManager.injector.get(DatabaseSessionManager)

            connection_database_repository: Repository[ConnectionDatabase] = Repository[ConnectionDatabase](
                database_session_manager)
            connection_repository: Repository[Connection] = Repository[Connection](
                database_session_manager)
            connection = connection_repository.first(Name=name, IsDeleted=0)
            connection_database = connection_database_repository.first(Connection=connection, IsDeleted=0)
            database_session_manager.session.delete(connection_database)
            database_session_manager.session.delete(connection)
            database_session_manager.commit()
