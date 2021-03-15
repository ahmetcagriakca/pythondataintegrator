import os
from unittest import TestCase
from infrastructor.IocManager import IocManager
from infrastructor.connection.file.FileProvider import FileProvider
from models.configs.ApiConfig import ApiConfig


class TestFileOperation(TestCase):
    def __init__(self, method_name='TestFileOperation'):
        super(TestFileOperation, self).__init__(method_name)

        from infrastructor.api.FlaskAppWrapper import FlaskAppWrapper
        from infrastructor.scheduler.JobScheduler import JobScheduler
        os.environ["PYTHON_ENVIRONMENT"] = 'test'
        self.root_directory = os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, os.pardir))
        IocManager.configure_startup(root_directory=self.root_directory,
                                     app_wrapper=FlaskAppWrapper,
                                     job_scheduler=JobScheduler)
        self.client = IocManager.app.test_client()

    def print_error_detail(self, data):
        print(data['message'] if 'message' in data else '')
        print(data['traceback'] if 'traceback' in data else '')
        print(data['message'] if 'message' in data else '')

    def test_get_data_count(self):
        file_provider = IocManager.injector.get(FileProvider)
        api_config: ApiConfig = IocManager.injector.get(ApiConfig)
        folder = os.path.join(api_config.root_directory, 'files')
        file_context = file_provider.get_file_context(folder)
        count = file_context.get_data_count(file_name='test.csv')
        assert count == 16

    def test_get_data(self):
        file_provider = IocManager.injector.get(FileProvider)
        api_config: ApiConfig = IocManager.injector.get(ApiConfig)
        folder = os.path.join(api_config.root_directory, 'files')
        file_context = file_provider.get_file_context_with_folder(folder)
        data = file_context.get_data(file_name='test.csv', names=["Id", "Name"], limit=10, start=2)
        assert len(data.index) == 10
        assert data['Id'][0] == 2

    # def test_copy_file_from_remote(self):
    #     from infrastructor.file.FileConnectionContext import FileConnectionContext
    #     file_manager: FileConnectionContext = IocManager.injector.get(FileConnectionContext)
    #     path = r'd:\Files\android_2020-01-01.csv'
    #     file = open(path)
    #     try:
    #         file_name = str(uuid.uuid4()) + ".csv"
    #         file_manager.write_binary_file_to_server(file=file, file_name=file_name)
    #     finally:
    #         if file is not None and hasattr(file, 'close'):
    #             file.close()
    #
    # def test_copy_file(self):
    #     from infrastructor.file.FileConnectionContext import FileConnectionContext
    #     file_manager: FileConnectionContext = IocManager.injector.get(FileConnectionContext)
    #     api_config: ApiConfig = IocManager.injector.get(ApiConfig)
    #     path = os.path.join(api_config.root_directory, 'files', 'android_2021-01-26.csv')
    #     file = open(path, 'rb')
    #     file1 = open(path, 'rb')
    #     try:
    #         file_name = str(uuid.uuid4()) + ".csv"
    #         file_manager.write_binary_file_to_server(file=file, file_name=file_name)
    #     finally:
    #         if file is not None and hasattr(file, 'close'):
    #             file.close()
    #
    # def test_read_file(self):
    #     path = r'd:\Files\android_2020-01-01.csv'
    #     csv_connector: FileConnectorStrategy = CsvFileConnector(path)
    #
    #     # count = csv_connector.get_count()
    #     df1 = csv_connector.read_data(row_count=10)
    #     df2 = csv_connector.read_data(row_count=100)
    #     df3 = csv_connector.read_data(row_count=10, skip_row_count=10)
    #     df3 = csv_connector.read_data(row_count=100, skip_row_count=34300)
    #     values1 = df1.values.tolist()
    #     values2 = df2.values.tolist()
    #     values3 = df3.values.tolist()
    #     for data in values1.tolist():
    #         print(data)
    #     # pandas.errors.EmptyDataError: No columns to parse from file
