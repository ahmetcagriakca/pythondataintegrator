from datetime import datetime
from unittest import TestCase

from infrastructor.IocManager import IocManager
from tests.integrationtests.common.TestManager import TestManager
from tests.integrationtests.operation.testdata.ScheduleJobTestData import ScheduleJobTestData


class TestScheduleJobResource(TestCase):
    def __init__(self, methodName='TestScheduleJobResource'):
        super(TestScheduleJobResource, self).__init__(methodName)
        self.test_manager = TestManager()

    def test_run_data_operation(self):
        expected = True
        IocManager.injector.get(IocManager.job_scheduler).run()
        self.test_manager.service_scenarios.create_test_connection(ScheduleJobTestData.test_job_connection)
        data_operation_response = self.test_manager.service_scenarios.create_test_operation(
            ScheduleJobTestData.test_data_operation)
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
                   ScheduleJobTestData.test_data_operation['Integrations'][0]["Integration"]["Code"]
            data_operation_job_id = response_data['Result']['Id']
            data_operation_job_execution = self.test_manager.service_scenarios.check_job_start(data_operation_job_id)
            start_date = data_operation_job_execution.StartDate.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            print(f'Job Started at:{start_date}')
            data_operation_job_execution = self.test_manager.service_scenarios.check_job_finish(data_operation_job_id)
            end_date = data_operation_job_execution.EndDate.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            print(f'Job Finished at:{end_date}')
            # checking execution successfully finished
            assert data_operation_job_execution.StatusId == 3
        except Exception as ex:
            assert True == False
        finally:
            # clean data_integration test operations
            self.test_manager.service_scenarios.clear_data_operation_job(data_operation_response["Result"]["Id"])
