import os
from time import time
from unittest import TestCase

from IocManager import IocManager
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.utils.Utils import Utils
from models.dao.operation import DataOperation
from models.dto.PagingModifier import PagingModifier


class TestHtmlTemplate(TestCase):

    def __init__(self, methodName='RunDataOperation'):
        super(TestHtmlTemplate, self).__init__(methodName)

        from infrastructure.api.FlaskAppWrapper import FlaskAppWrapper
        os.environ["PYTHON_ENVIRONMENT"] = 'test'
        IocManager.set_app_wrapper(app_wrapper=FlaskAppWrapper)
        IocManager.initialize()
        self.client = IocManager.app.test_client()

    def print_error_detail(self, data):
        print(data['message'] if 'message' in data else '')
        print(data['traceback'] if 'traceback' in data else '')
        print(data['message'] if 'message' in data else '')

    def test_TestHtmlTemplate(self):
        from domain.operation.page.DataOperationPage import DataOperationPage
        data_operation_page: DataOperationPage = IocManager.injector.get(DataOperationPage)
        result = data_operation_page.render()

    def test_TestHtmlTemplate(self):
        from domain.operation.page.DataOperationPage import DataOperationPage
        repository_provider: RepositoryProvider = IocManager.injector.get(RepositoryProvider)
        data_operation_repository = repository_provider.get(DataOperation)

