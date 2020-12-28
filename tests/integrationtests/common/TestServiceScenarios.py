from infrastructor.IocManager import IocManager
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from models.dao.connection.Connection import Connection
from models.dao.connection.ConnectionDatabase import ConnectionDatabase
from models.dao.integration.DataIntegration import DataIntegration
from models.dao.operation import DataOperation, DataOperationJob
from tests.integrationtests.common.TestServiceEndpoints import TestServiceEndpoints


class TestServiceScenarios:
    def __init__(self,
                 service_endpoints: TestServiceEndpoints,
                 ioc_manager: IocManager):
        self.ioc_manager = ioc_manager
        self.service_endpoints = service_endpoints

    def clear_connection(self, name):

        database_session_manager: DatabaseSessionManager = self.ioc_manager.injector.get(
            DatabaseSessionManager)
        connection_repository: Repository[Connection] = Repository[Connection](
            database_session_manager)
        connection = connection_repository.first(Name=name)
        database_session_manager.session.delete(connection.Database)
        database_session_manager.session.delete(connection)
        database_session_manager.commit()

    def clear_integration(self, code):
        database_session_manager: DatabaseSessionManager = self.ioc_manager.injector.get(
            DatabaseSessionManager)
        data_integration_repository: Repository[DataIntegration] = Repository[DataIntegration](
            database_session_manager)
        data_integration = data_integration_repository.first(Code=code)

        for data_integration_column in data_integration.Columns:
            database_session_manager.session.delete(data_integration_column)
        for data_integration_execution_job in data_integration.ExecutionJobs:
            database_session_manager.session.delete(data_integration_execution_job)
        for data_integration_connection in data_integration.Connections:
            database_session_manager.session.delete(data_integration_connection)

        database_session_manager.session.delete(data_integration)
        database_session_manager.commit()

    def clear_operation(self, name):
        database_session_manager: DatabaseSessionManager = self.ioc_manager.injector.get(
            DatabaseSessionManager)
        data_integration_repository: Repository[DataOperation] = Repository[DataOperation](
            database_session_manager)
        data_operation = data_integration_repository.first(Name=name)

        for data_operation_integration in data_operation.Integrations:
            database_session_manager.session.delete(data_operation_integration)
        for data_operation_job in data_operation.DataOperationJobs:
            database_session_manager.session.delete(data_operation_job)

        database_session_manager.session.delete(data_operation)
        database_session_manager.commit()

    def clear_data_operation_job(self, data_operation_id):
        database_session_manager: DatabaseSessionManager = self.ioc_manager.injector.get(
            DatabaseSessionManager)
        data_operation_job_repository: Repository[DataOperationJob] = Repository[DataOperationJob](
            database_session_manager)

        data_operation_job = data_operation_job_repository.first(IsDeleted=0,
                                                                 DataOperationId=data_operation_id)
        if data_operation_job is  None:
            return
        if data_operation_job.DataOperationJobExecutions is not None:
            for data_operation_job_execution in data_operation_job.DataOperationJobExecutions:
                database_session_manager.session.delete(data_operation_job_execution)

        database_session_manager.session.delete(data_operation_job.ApSchedulerJob)
        database_session_manager.session.delete(data_operation_job)
        database_session_manager.commit()

    def create_test_connection(self, test_data_connection):
        database_session_manager: DatabaseSessionManager = self.ioc_manager.injector.get(
            DatabaseSessionManager)
        connection_repository: Repository[Connection] = Repository[Connection](
            database_session_manager)

        connection = connection_repository.first(Name=test_data_connection["Name"])
        if connection is not None:
            self.clear_connection(name=test_data_connection["Name"])
        response_data = self.service_endpoints.insert_connection_database(test_data_connection)

    def create_test_integration(self, test_data_integration):
        database_session_manager: DatabaseSessionManager = self.ioc_manager.injector.get(
            DatabaseSessionManager)
        data_integration_repository: Repository[DataIntegration] = Repository[DataIntegration](
            database_session_manager)
        data_integration = data_integration_repository.first(Code=test_data_integration["Code"])
        if data_integration is not None:
            self.clear_integration(code=test_data_integration["Code"])
        response_data = self.service_endpoints.insert_data_integration(test_data_integration)
        return response_data

    def create_test_operation(self, test_data_operation):
        database_session_manager: DatabaseSessionManager = self.ioc_manager.injector.get(
            DatabaseSessionManager)
        data_operation_repository: Repository[DataOperation] = Repository[DataOperation](
            database_session_manager)
        data_operation = data_operation_repository.first(Name=test_data_operation["Name"])
        if data_operation is not None:
            self.clear_operation(name=test_data_operation["Name"])
        response_data = self.service_endpoints.insert_data_operation(test_data_operation)
        return response_data
