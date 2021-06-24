import os
from time import time
from unittest import TestCase

from IocManager import IocManager
from infrastructor.utils.Utils import Utils
from models.dto.PagingModifier import PagingModifier


class TestDataOperation(TestCase):

    def __init__(self, methodName='RunDataOperation'):
        super(TestDataOperation, self).__init__(methodName)

        from infrastructor.api.FlaskAppWrapper import FlaskAppWrapper
        os.environ["PYTHON_ENVIRONMENT"] = 'test'
        IocManager.set_app_wrapper(app_wrapper=FlaskAppWrapper)
        IocManager.initialize()
        self.client = IocManager.app.test_client()

    def print_error_detail(self, data):
        print(data['message'] if 'message' in data else '')
        print(data['traceback'] if 'traceback' in data else '')
        print(data['message'] if 'message' in data else '')

    def test_folders1(self):
        indexer = ':{index}'
        st= indexer.format(index=5)
        assert st == ':5'
        indexer = '%s'
        st= indexer.format(index=5)
        assert st == '%s'
        indexer = '?'
        st= indexer.format(index=5)
        assert st == '?'
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
        end = limit
        start = 0
        paging_modifiers = []
        while True:
            if end != limit and end - data_count > limit:
                break
            paging_modifier = PagingModifier(End=end, Start=start)
            paging_modifiers.append(paging_modifier)
            end += limit
            start += limit
        for li in paging_modifiers:
            print(f"{li.End} - {li.End}")

    def test_parallel_data_operation(self):
        start = time()
        from domain.operation.services.DataOperationService import DataOperationService
        data_operation_service: DataOperationService = IocManager.injector.get(DataOperationService)
        result = data_operation_service.start_operation('TEST_OPERATION', 0)
        print(result)
        end = time()
        print(f"EndTime :{end}")
        print(f"TotalTime :{end - start}")

    def test_data_operation(self):
        start = time()
        from domain.operation.services.DataOperationService import DataOperationService
        data_operation_service: DataOperationService = IocManager.injector.get(DataOperationService)
        result = data_operation_service.start_operation('LOCAL_LOG', 0)
        print(result)
        end = time()
        print(f"EndTime :{end}")
        print(f"TotalTime :{end - start}")

    def test_start_operation(self):
        start = time()
        from domain.operation.services.DataOperationService import DataOperationService
        data_operation_service: DataOperationService = IocManager.injector.get(DataOperationService)
        result = data_operation_service.start_operation('LOCAL_LOG', 0)
        print(result)
        end = time()
        print(f"EndTime :{end}")
        print(f"TotalTime :{end - start}")
