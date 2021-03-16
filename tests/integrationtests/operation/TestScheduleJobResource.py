from unittest import TestCase
from tests.integrationtests.common.TestManager import TestManager
from tests.integrationtests.operation.testdata import ScheduleJobTestData
from tests.integrationtests.operation.testdata.ScheduleJobFileTestData import ScheduleJobFileTestData


class TestScheduleJobResource(TestCase):
    def __init__(self, methodName='TestScheduleJobResource'):
        super(TestScheduleJobResource, self).__init__(methodName)
        self.test_manager = TestManager()

    def test_run_data_operation(self):
        connections = [
            ScheduleJobTestData.test_job_connection,
            ScheduleJobTestData.test_job_connection,
        ]
        data_operation = ScheduleJobTestData.test_data_operation

        self.test_manager.service_scenarios.run_data_operation(connections=connections,
                                                               data_operation=data_operation)

    def test_run_file_data_operation(self):
        connection_databases = [
            ScheduleJobFileTestData.test_job_connection,
        ]

        connection_files = [
            ScheduleJobFileTestData.test_file_connection,
        ]

        data_operation = ScheduleJobFileTestData.test_data_operation

        self.test_manager.service_scenarios.run_data_operation_without_schedule(connections=connection_databases,
                                                                                data_operation=data_operation,
                                                                                connection_files=connection_files)
