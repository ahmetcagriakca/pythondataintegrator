import os
from time import time
from unittest import TestCase

from pdip.dependency.container import DependencyContainer
from pdip.cryptography import CryptoService
from pdip.utils import Utils


class TestDataOperation(TestCase):

    def __init__(self, methodName='RunDataOperation'):
        super(TestDataOperation, self).__init__(methodName)

        from infrastructure.api.FlaskAppWrapper import FlaskAppWrapper
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

    def test_decrypt(self):
        crypto_service: CryptoService = IocManager.injector.get(CryptoService)

        text=crypto_service.decrypt_code("gAAAAABgNl2U4gFI97zrN5Svwj287Y7O0EbFL56vKyhyYP_n1dmUOYfzGvPM90_2FFkxqW4QBTIayyRM5Hy-6969dL80ra5SNA==")
        print(text)