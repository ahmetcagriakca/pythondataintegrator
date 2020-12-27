import json
import os
from unittest import TestCase

from infrastructor.IocManager import IocManager
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from models.dao.connection.Connection import Connection
from models.dao.connection.ConnectionDatabase import ConnectionDatabase


class TestConnectionResuource(TestCase):
    def __init__(self, methodName='TestConnectionResuource'):
        super(TestConnectionResuource, self).__init__(methodName)

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

    def test_get_connection(self):
        response = self.client.get(
            '/api/Connection',
            content_type='application/json',
        )

        response_data = json.loads(response.get_data(as_text=True))
        print(response_data)
        assert response.status_code == 200
        self.print_error_detail(response_data)
        assert response_data['IsSuccess'] == True

    def delete_connection(self, request):
        data = json.dumps(request)
        response = self.client.delete(
            '/api/Connection',
            data=data,
            content_type='application/json',
        )
        response_data = json.loads(response.get_data(as_text=True))
        print(response_data)
        assert response.status_code == 200
        self.print_error_detail(response_data)
        return response_data

    def test_get_connection(self):
        id=1
        test_data = {"Id": id}
        response_data= self.delete_connection(test_data)
        assert response_data["Message"] == "Connection Removed Successfully"
        database_session_manager: DatabaseSessionManager = IocManager.injector.get(DatabaseSessionManager)

        connection_database_repository: Repository[ConnectionDatabase] = Repository[ConnectionDatabase](
            database_session_manager)
        connection_repository: Repository[Connection] = Repository[Connection](
            database_session_manager)
        connection = connection_repository.first(Id=id)
        connection_database = connection_database_repository.first(Connection=connection)
        connection.IsDeleted=0
        connection_database.IsDeleted=0
        database_session_manager.commit()