import os
from time import time
from unittest import TestCase

from pdip.base import Pdi

from domain.operation.commands.SendDataOperationFinishMailCommand import SendDataOperationFinishMailCommand


class TestDataOperation(TestCase):

    def setUp(self):
        os.environ["PYTHON_ENVIRONMENT"] = 'test'
        root_directory = os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, os.pardir))
        self.pdi = Pdi(root_directory=root_directory)
        # self.client = self.pdi.get(FlaskAppWrapper).test_client()

    def tearDown(self):
        if hasattr(self, 'pdi') and self.pdi is not None:
            self.pdi.cleanup()
            del self.pdi
        return super().tearDown()

    def __init__(self, methodName='RunDataOperation'):
        super(TestDataOperation, self).__init__(methodName)

        # IocManager.initialize()

    def print_error_detail(self, data):
        print(data['message'] if 'message' in data else '')
        print(data['traceback'] if 'traceback' in data else '')
        print(data['message'] if 'message' in data else '')

    def test_start_operation(self):
        start = time()
        from domain.operation.execution.services.OperationExecution import OperationExecution
        from domain.operation.commands.CreateExecutionCommand import CreateExecutionCommand
        data_operation_id = 61
        job_id = 675
        execution_id = self.pdi.get(CreateExecutionCommand).execute(data_operation_id=data_operation_id,
                                                                    job_id=job_id)
        operation_execution: OperationExecution = self.pdi.get(OperationExecution)
        result = operation_execution.start(data_operation_id=data_operation_id, job_id=job_id,
                                           data_operation_job_execution_id=execution_id)

        print(result)
        end = time()
        print(f"EndTime :{end}")
        print(f"TotalTime :{end - start}")

    def test_send_data_operation_finish_mail_command(self):
        data_operation_job_execution_id = 960
        send_data_operation_finish_mail_command = self.pdi.get(SendDataOperationFinishMailCommand)
        send_data_operation_finish_mail_command.execute(data_operation_job_execution_id=data_operation_job_execution_id)
