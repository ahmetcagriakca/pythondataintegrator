import json
import os
import time
from datetime import datetime
from unittest import TestCase

from infrastructor.IocManager import IocManager
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from models.configs.ApiConfig import ApiConfig
from models.configs.DatabaseConfig import DatabaseConfig
from models.dao.aps import ApSchedulerJob
from models.dao.operation import DataOperation, DataOperationJob, DataOperationJobExecution
from tests.integrationtests.common.TestManager import TestManager
from tests.integrationtests.connection.testdata.ConnectionTestData import ConnectionTestData
from tests.integrationtests.integration.testdata.DataIntegrationTestData import DataIntegrationTestData
from tests.integrationtests.operation.testdata.DataOperationTestData import DataOperationTestData
from tests.integrationtests.operation.testdata.ScheduleJobTestData import ScheduleJobTestData


class TestScheduleJobResource(TestCase):
    def __init__(self, methodName='TestScheduleJobResource'):
        super(TestScheduleJobResource, self).__init__(methodName)
        self.test_manager = TestManager()

    def check_job_start(self, data_operation_job_id) -> DataOperationJobExecution:
        database_session_manager: DatabaseSessionManager = self.test_manager.ioc_manager.injector.get(
            DatabaseSessionManager)
        data_operation_job_execution_repository: Repository[DataOperationJobExecution] = Repository[
            DataOperationJobExecution](database_session_manager)
        data_operation_job_execution = data_operation_job_execution_repository.first(
            DataOperationJobId=data_operation_job_id)
        if data_operation_job_execution is None:
            time.sleep(2)
            data_operation_job_execution = self.check_job_start(data_operation_job_id)
        return data_operation_job_execution

    def check_job_finish(self, data_operation_job_id) -> DataOperationJobExecution:
        # database_session_manager: DatabaseSessionManager = self.test_manager.ioc_manager.injector.get(
        #     DatabaseSessionManager)
        api_config: DatabaseSessionManager = self.test_manager.ioc_manager.config_manager.get(
            ApiConfig)
        database_config: DatabaseSessionManager = self.test_manager.ioc_manager.config_manager.get(
            DatabaseConfig)
        database_session_manager = DatabaseSessionManager(api_config=api_config, database_config=database_config)
        database_session_manager.session = database_session_manager.session_factory()
        data_operation_job_execution_repository: Repository[DataOperationJobExecution] = Repository[
            DataOperationJobExecution](database_session_manager)
        data_operation_job_execution = data_operation_job_execution_repository.first(
            DataOperationJobId=data_operation_job_id)
        # del database_session_manager
        return data_operation_job_execution

    def test_schedule_job(self):
        expected = True
        IocManager.injector.get(IocManager.job_scheduler).run()
        self.test_manager.service_scenarios.create_test_connection(ScheduleJobTestData.test_job_connection)
        data_integration_response = self.test_manager.service_scenarios.create_test_integration(
            ScheduleJobTestData.test_job_integration)
        data_integration_response = self.test_manager.service_scenarios.create_test_integration(
            ScheduleJobTestData.test_job_integration_for_update)
        data_integration_response = self.test_manager.service_scenarios.create_test_integration(
            ScheduleJobTestData.test_job_integration_for_target_query)
        data_operation_response = self.test_manager.service_scenarios.create_test_operation(
            ScheduleJobTestData.test_job_data_operation)
        try:
            run_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            job_request = {
                "OperationName": data_operation_response["Result"]['Name'],
                "RunDate": run_date
            }
            response_data = self.test_manager.service_endpoints.run_schedule_job_operation(
                job_request)
            assert response_data['IsSuccess'] == expected
            assert response_data['Result']['DataOperation']['Name'] == job_request['OperationName']
            assert response_data['Result']['DataOperation']['Integrations'][0]["Integration"]["Code"] == \
                   ScheduleJobTestData.test_job_data_operation['Integrations'][0]["Code"]
            data_operation_job_execution: DataOperationJobExecution = self.check_job_start(
                response_data['Result']['Id'])
            start_date = data_operation_job_execution.StartDate.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            print(f'Job Started at:{start_date}')
            while True:
                data_operation_job_execution: DataOperationJobExecution = self.check_job_finish(
                    response_data['Result']['Id'])

                # checking job execution finish
                if data_operation_job_execution is not None and (
                        data_operation_job_execution.StatusId != 3 and data_operation_job_execution.StatusId != 4
                ):
                    time.sleep(5)
                else:
                    break
            end_date = data_operation_job_execution.EndDate.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            print(f'Job Finished at:{end_date}')
            # checking execution successfully finished
            assert data_operation_job_execution.StatusId == 3
        except Exception as ex:
            assert True == False
        finally:
            # clean integration test operations
            self.test_manager.service_scenarios.clear_data_operation_job(data_operation_response["Result"]["Id"])
