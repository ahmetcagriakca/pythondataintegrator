from unittest import TestCase
from tests.integrationtests.common.TestManager import TestManager
from tests.integrationtests.operation.testdata import TestScheduleJobData
from tests.integrationtests.operation.testdata.TestScheduleJobFileData import TestScheduleJobFileData
from tests.integrationtests.operation.testdata.TestScheduleJobQueueData import TestScheduleJobQueueData


class TestScheduleJobResource(TestCase):
    def __init__(self, methodName='TestScheduleJobResource'):
        super(TestScheduleJobResource, self).__init__(methodName)
        self.test_manager = TestManager()

    def test_run_data_operation(self):
        connection_databases = [
            TestScheduleJobData.test_job_connection,
            TestScheduleJobData.test_job_connection,
        ]
        data_operation = TestScheduleJobData.test_data_operation

        self.test_manager.service_scenarios.run_data_operation(
            data_operation=data_operation,
            connection_databases=connection_databases,
        )

    def test_run_file_data_operation(self):
        connection_databases = [
            TestScheduleJobFileData.test_job_connection,
        ]

        connection_files = [
            TestScheduleJobFileData.test_file_connection,
        ]

        data_operation = TestScheduleJobFileData.test_data_operation

        self.test_manager.service_scenarios.run_data_operation_without_schedule(
            data_operation=data_operation,
            connection_databases=connection_databases,
            connection_files=connection_files)

    def test_run_queue_data_operation(self):
        connection_databases = [
            TestScheduleJobQueueData.test_job_connection,
        ]

        connection_queues = [
            TestScheduleJobQueueData.test_queue_connection,
        ]

        data_operation = TestScheduleJobQueueData.test_data_operation

        self.test_manager.service_scenarios.run_data_operation_without_schedule(
            data_operation=data_operation,
            connection_databases=connection_databases,
            connection_queues=connection_queues)
