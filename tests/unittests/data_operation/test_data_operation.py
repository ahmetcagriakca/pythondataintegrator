import os
from time import time
from unittest import TestCase

from infrastructor.IocManager import IocManager
from infrastructor.utils.Utils import Utils
from models.dto.LimitModifier import LimitModifier


class TestDataOperation(TestCase):

    def __init__(self, methodName='RunDataOperation'):
        super(TestDataOperation, self).__init__(methodName)

        from infrastructor.api.FlaskAppWrapper import FlaskAppWrapper
        from infrastructor.scheduler.JobScheduler import JobScheduler
        os.environ["PYTHON_ENVIRONMENT"] = 'test'
        self.root_directory = os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))
        IocManager.configure_startup(root_directory=self.root_directory,
                                     app_wrapper=FlaskAppWrapper,
                                     job_scheduler=JobScheduler)
        self.client = IocManager.app.test_client()

    def print_error_detail(self, data):
        print(data['message'] if 'message' in data else '')
        print(data['traceback'] if 'traceback' in data else '')
        print(data['message'] if 'message' in data else '')

    def test_folders1(self):
        folders = Utils.find_sub_folders(self.root_directory + '\\models\\dao')
        module_list, module_attr_list = Utils.get_modules(folders)
        for module in module_list:
            print(module)

    def test_limit_data(self):
        import socket
        print(socket.gethostname())
        socket.get
        data_count = 700000
        limit = 10000
        top_limit = limit
        sub_limit = 0
        limit_modifiers = []
        while True:
            if top_limit != limit and top_limit - data_count > limit:
                break
            limit_modifier = LimitModifier(top_limit=top_limit, sub_limit=sub_limit)
            limit_modifiers.append(limit_modifier)
            top_limit += limit
            sub_limit += limit
        for li in limit_modifiers:
            print(f"{li.sub_limit} - {li.top_limit}")

    def test_parallel_data_operation(self):
        start = time()
        print(f"StartTime :{start}")
        from domain.pdi.services.DataOperationService import DataOperationService
        data_operation_service: DataOperationService = IocManager.injector.get(DataOperationService)
        result = data_operation_service.start_operation('CI_TRANSFER_TEST', 0)
        print(result)
        end = time()
        print(f"EndTime :{end}")
        print(f"TotalTime :{end - start}")

    def test_data_operation(self):
        start = time()
        print(f"StartTime :{start}")
        from domain.pdi.services.DataOperationService import DataOperationService
        data_operation_service: DataOperationService = IocManager.injector.get(DataOperationService)
        result = data_operation_service.start_operation('LOCAL_LOG', 0)
        print(result)
        end = time()
        print(f"EndTime :{end}")
        print(f"TotalTime :{end - start}")

    def test_start_operation(self):
        start = time()
        print(f"StartTime :{start}")
        from domain.pdi.services.DataOperationService import DataOperationService
        data_operation_service: DataOperationService = IocManager.injector.get(DataOperationService)
        result = data_operation_service.start_operation('LOCAL_LOG', 0)
        print(result)
        end = time()
        print(f"EndTime :{end}")
        print(f"TotalTime :{end - start}")
