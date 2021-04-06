import time
from datetime import datetime

from domain.operation.execution.services.OperationExecution import OperationExecution
from domain.operation.services.DataOperationJobService import DataOperationJobService
from domain.operation.services.DataOperationService import DataOperationService
from infrastructor.IocManager import IocManager
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from models.configs.DatabaseConfig import DatabaseConfig
from models.dao.aps import ApSchedulerJob
from models.dao.connection.Connection import Connection
from models.dao.integration.DataIntegration import DataIntegration
from models.dao.operation import DataOperation, DataOperationJob, DataOperationJobExecution
from models.dao.secret import Secret
from tests.integrationtests.common.TestServiceEndpoints import TestServiceEndpoints


class TestServiceScenarios:
    def __init__(self,
                 service_endpoints: TestServiceEndpoints,
                 ioc_manager: IocManager):
        self.ioc_manager = ioc_manager
        self.service_endpoints = service_endpoints

    def get_data_operation(self, name):
        data_operation_service: DataOperationService = self.ioc_manager.injector.get(
            DataOperationService)
        data_operation = data_operation_service.get_by_name(name=name)
        return data_operation

    def clear_secret(self, id):
        database_session_manager: DatabaseSessionManager = self.ioc_manager.injector.get(
            DatabaseSessionManager)
        secret_repository: Repository[Secret] = Repository[Secret](
            database_session_manager)
        secret = secret_repository.first(Id=id)
        for secret_source in secret.SecretSources:
            for basic_authentication in secret_source.SecretSourceBasicAuthentications:
                database_session_manager.session.delete(basic_authentication)
            database_session_manager.session.delete(secret_source)
        database_session_manager.session.delete(secret)

    def clear_connection(self, name):

        database_session_manager: DatabaseSessionManager = self.ioc_manager.injector.get(
            DatabaseSessionManager)
        connection_repository: Repository[Connection] = Repository[Connection](
            database_session_manager)
        connection = connection_repository.first(Name=name)
        for connection_secret in connection.ConnectionSecrets:
            self.clear_secret(connection_secret.SecretId)
            database_session_manager.session.delete(connection_secret)
        if connection.ConnectionServers is not None:
            for connection_server in connection.ConnectionServers:
                database_session_manager.session.delete(connection_server)
        if connection.Database is not None:
            database_session_manager.session.delete(connection.Database)
        if connection.File is not None:
            database_session_manager.session.delete(connection.File)
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
        for data_integration_connection in data_integration.Connections:
            database_session_manager.session.delete(data_integration_connection)

        database_session_manager.session.delete(data_integration)
        database_session_manager.commit()

    def clear_operation(self, name):
        database_session_manager: DatabaseSessionManager = self.ioc_manager.injector.get(
            DatabaseSessionManager)
        data_operation_repository: Repository[DataOperation] = Repository[DataOperation](
            database_session_manager)
        data_operation = data_operation_repository.first(Name=name)
        if data_operation is None:
            return

        for data_operation_contact in data_operation.Contacts:
            database_session_manager.session.delete(data_operation_contact)

        for data_operation_integration in data_operation.Integrations:
            data_integration = data_operation_integration.DataIntegration

            for data_integration_column in data_integration.Columns:
                database_session_manager.session.delete(data_integration_column)
            for data_integration_connection in data_integration.Connections:
                database_session_manager.session.delete(data_integration_connection)
            database_session_manager.session.delete(data_integration)

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
        if data_operation_job is None:
            return
        if data_operation_job.DataOperationJobExecutions is not None:
            for data_operation_job_execution in data_operation_job.DataOperationJobExecutions:
                database_session_manager.session.delete(data_operation_job_execution)

        database_session_manager.session.delete(data_operation_job.ApSchedulerJob)
        database_session_manager.session.delete(data_operation_job)
        database_session_manager.commit()

    def create_test_connection_database(self, test_data_connection):
        database_session_manager: DatabaseSessionManager = self.ioc_manager.injector.get(
            DatabaseSessionManager)
        connection_repository: Repository[Connection] = Repository[Connection](
            database_session_manager)

        connection = connection_repository.first(Name=test_data_connection["Name"])
        if connection is not None:
            self.clear_connection(name=test_data_connection["Name"])
        response_data = self.service_endpoints.create_connection_database(test_data_connection)

    def create_test_connection_file(self, test_data_connection):
        database_session_manager: DatabaseSessionManager = self.ioc_manager.injector.get(
            DatabaseSessionManager)
        connection_repository: Repository[Connection] = Repository[Connection](
            database_session_manager)

        connection = connection_repository.first(Name=test_data_connection["Name"])
        if connection is not None:
            self.clear_connection(name=test_data_connection["Name"])
        response_data = self.service_endpoints.create_connection_file(test_data_connection)

    def create_test_connection_queue(self, test_data_connection):
        database_session_manager: DatabaseSessionManager = self.ioc_manager.injector.get(
            DatabaseSessionManager)
        connection_repository: Repository[Connection] = Repository[Connection](
            database_session_manager)

        connection = connection_repository.first(Name=test_data_connection["Name"])
        if connection is not None:
            self.clear_connection(name=test_data_connection["Name"])
        response_data = self.service_endpoints.create_connection_queue(test_data_connection)

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

    def get_data_operation_job_execution(self, data_operation_job_id) -> DataOperationJobExecution:
        database_config: DatabaseSessionManager = self.ioc_manager.config_manager.get(
            DatabaseConfig)
        database_session_manager = DatabaseSessionManager(database_config=database_config)
        database_session_manager.session = database_session_manager.session_factory()
        data_operation_job_execution_repository: Repository[DataOperationJobExecution] = Repository[
            DataOperationJobExecution](database_session_manager)
        data_operation_job_execution = data_operation_job_execution_repository.first(
            DataOperationJobId=data_operation_job_id)
        return data_operation_job_execution

    def check_job_start(self, data_operation_job_id) -> DataOperationJobExecution:
        while True:
            data_operation_job_execution: DataOperationJobExecution = self.get_data_operation_job_execution(
                data_operation_job_id)
            # checking job execution started
            if data_operation_job_execution is not None:
                time.sleep(5)
                return data_operation_job_execution

    def check_job_finish(self, data_operation_job_id) -> DataOperationJobExecution:
        while True:
            data_operation_job_execution: DataOperationJobExecution = self.get_data_operation_job_execution(
                data_operation_job_id)
            # checking job execution finish
            if data_operation_job_execution is not None and (
                    data_operation_job_execution.StatusId != 3 and data_operation_job_execution.StatusId != 4
            ):
                time.sleep(10)
            else:
                return data_operation_job_execution

    def create_data_operation(self, data_operation, connection_databases=None, connection_files=None, connection_queues=None):
        if connection_databases is not None:
            for connection_database in connection_databases:
                self.create_test_connection_database(connection_database)
        if connection_files is not None:
            for connection_file in connection_files:
                self.create_test_connection_file(connection_file)
        if connection_queues is not None:
            for connection_queue in connection_queues:
                self.create_test_connection_queue(connection_queue)
        self.create_test_operation(data_operation)

    def run_job_without_schedule(self, data_operation_name):
        expected = True
        try:
            data_operation = self.get_data_operation(name=data_operation_name)
            operation_execution = IocManager.injector.get(OperationExecution)
            ap_scheduler_job = ApSchedulerJob(JobId='temp', NextRunTime=None, FuncRef='None')
            data_operation_job_service = IocManager.injector.get(DataOperationJobService)
            database_session_manager = IocManager.injector.get(DatabaseSessionManager)
            ap_scheduler_job_repository = Repository[ApSchedulerJob](database_session_manager)
            ap_scheduler_job_repository.insert(ap_scheduler_job)

            data_operation_job = data_operation_job_service.insert_data_operation_job(
                ap_scheduler_job=ap_scheduler_job,
                data_operation=data_operation,
                cron=None, start_date=datetime.now(),
                end_date=None)
            database_session_manager.commit()
            operation_execution.start(data_operation_id=data_operation.Id,
                                      job_id=ap_scheduler_job.Id)
        except Exception as ex:
            import traceback
            tb = traceback.format_exc()
            print(tb)
            assert True == False

    def run_job(self, data_operation_name):
        expected = True
        try:
            IocManager.injector.get(IocManager.job_scheduler).run()
            run_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            job_request = {
                "OperationName": data_operation_name,
                "RunDate": run_date
            }
            response_data = self.service_endpoints.run_schedule_job_operation(
                job_request)
            assert response_data['IsSuccess'] == expected
            assert response_data['Result']['DataOperation']['Name'] == job_request['OperationName']
            data_operation_job_id = response_data['Result']['Id']
            data_operation_job_execution = self.check_job_start(data_operation_job_id)
            start_date = data_operation_job_execution.StartDate.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            print(f'Job Started at:{start_date}')
            data_operation_job_execution = self.check_job_finish(data_operation_job_id)
            end_date = data_operation_job_execution.EndDate.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            print(f'Job Finished at:{end_date}')
            # checking execution successfully finished
            assert data_operation_job_execution.StatusId == 3
        except Exception as ex:
            assert True == False
        # finally:
        #     # clean data_integration test operations
        #     self.clear_data_operation_job(data_operation_response["Result"]["Id"])

    def run_data_operation(self, connections, data_operation, connection_files):
        self.create_data_operation(connections, data_operation, connection_files)
        self.run_job(data_operation['Name'])

    def run_data_operation_without_schedule(self, data_operation, connection_databases=None, connection_files=None,
                                            connection_queues=None):
        self.create_data_operation(data_operation, connection_databases, connection_files, connection_queues)
        self.run_job_without_schedule(data_operation['Name'])
