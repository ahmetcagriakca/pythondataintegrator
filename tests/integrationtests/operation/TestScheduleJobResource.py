from unittest import TestCase
from tests.integrationtests.common.TestManager import TestManager
from tests.integrationtests.operation.testdata import ScheduleJobTestData


class TestScheduleJobResource(TestCase):
    def __init__(self, methodName='TestScheduleJobResource'):
        super(TestScheduleJobResource, self).__init__(methodName)
        self.test_manager = TestManager()

    def test_run_data_operation(self):
        connections = [
            ScheduleJobTestData.test_job_connection,
        ]
        data_operation = ScheduleJobTestData.test_data_operation

        self.test_manager.service_scenarios.run_data_operation(connections=connections,
                                                               data_operation=data_operation)
