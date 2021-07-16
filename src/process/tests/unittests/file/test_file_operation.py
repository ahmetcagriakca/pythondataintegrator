import os
import uuid
from unittest import TestCase

from IocManager import IocManager
from infrastructure.connection.file.FileContext import FileContext
from infrastructure.connection.file.FileProvider import FileProvider
from infrastructure.connection.file.connectors.FileConnector import FileConnector
from models.configs.ApplicationConfig import ApplicationConfig


class TestFileOperation(TestCase):
    def __init__(self, method_name='TestFileOperation'):
        super(TestFileOperation, self).__init__(method_name)

        os.environ["PYTHON_ENVIRONMENT"] = 'test'
        IocManager.initialize()

    def print_error_detail(self, data):
        print(data['message'] if 'message' in data else '')
        print(data['traceback'] if 'traceback' in data else '')
        print(data['message'] if 'message' in data else '')

    def test_get_data_count(self):
        file_provider = IocManager.injector.get(FileProvider)
        application_config: ApplicationConfig = IocManager.injector.get(ApplicationConfig)
        folder = os.path.join(application_config.root_directory, 'files')
        file_context = file_provider.get_context(folder)
        count = file_context.get_data_count(file_name='test.csv')
        assert count == 16

    def test_get_data(self):
        file_provider = IocManager.injector.get(FileProvider)
        application_config: ApplicationConfig = IocManager.injector.get(ApplicationConfig)
        folder = os.path.join(application_config.root_directory, 'files')
        file_context = file_provider.get_file_context_with_folder(folder)
        data = file_context.get_data(file_name='test.csv', names=["Id", "Name"], limit=10, start=2)
        assert len(data.index) == 10
        assert data['Id'][0] == 2

    def test_copy_file_from_remote(self):
        file_manager: FileContext = IocManager.injector.get(FileContext)
        path = r'd:\Files\android_2020-01-01.csv'
        file = open(path)
        try:
            file_name = str(uuid.uuid4()) + ".csv"
            file_manager.write_binary_file_to_server(file=file, file_name=file_name)
        finally:
            if file is not None and hasattr(file, 'close'):
                file.close()

    def test_copy_file(self):
        file_manager: FileContext = IocManager.injector.get(FileContext)
        application_config: ApplicationConfig = IocManager.injector.get(ApplicationConfig)
        path = os.path.join(application_config.root_directory, 'files', 'android_2021-01-26.csv')
        file = open(path, 'rb')
        file1 = open(path, 'rb')
        try:
            file_name = str(uuid.uuid4()) + ".csv"
            file_manager.write_binary_file_to_server(file=file, file_name=file_name)
        finally:
            if file is not None and hasattr(file, 'close'):
                file.close()

    def test_read_file(self):
        path = r'd:\Files\android_2020-01-01.csv'
        csv_connector: FileConnector = FileConnector(path)

        # count = csv_connector.get_count()
        df1 = csv_connector.read_data(row_count=10)
        df2 = csv_connector.read_data(row_count=100)
        df3 = csv_connector.read_data(row_count=10, skip_row_count=10)
        df3 = csv_connector.read_data(row_count=100, skip_row_count=34300)
        values1 = df1.values.tolist()
        values2 = df2.values.tolist()
        values3 = df3.values.tolist()
        for data in values1.tolist():
            print(data)
        # pandas.errors.EmptyDataError: No columns to parse from file
