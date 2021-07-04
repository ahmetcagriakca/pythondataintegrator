import json
import os
import datetime
from time import time
from unittest import TestCase

from IocManager import IocManager
from domain.operation.execution.services.OperationExecution import OperationExecution
from domain.operation.services.DataOperationService import DataOperationService
from infrastructor.data.RepositoryProvider import RepositoryProvider
from infrastructor.utils.ConfigManager import ConfigManager
from infrastructor.utils.Utils import Utils
from models.configs.ApplicationConfig import ApplicationConfig
from models.configs.DatabaseConfig import DatabaseConfig
from models.dao.operation import DataOperation
from models.dao.secret import AuthenticationType
from models.dto.PagingModifier import PagingModifier


class TestDataOperation(TestCase):

    def __init__(self, methodName='RunDataOperation'):
        super(TestDataOperation, self).__init__(methodName)

        os.environ["PYTHON_ENVIRONMENT"] = 'test'
        IocManager.initialize()

    def print_error_detail(self, data):
        print(data['message'] if 'message' in data else '')
        print(data['traceback'] if 'traceback' in data else '')
        print(data['message'] if 'message' in data else '')

    def test_config_value(self):
        config_value = IocManager.config_manager.get(DatabaseConfig)
        injector_value = IocManager.injector.get(DatabaseConfig)
        assert config_value.application_name is None
        assert injector_value.application_name is None
        application_config: ApplicationConfig = IocManager.config_manager.get(ApplicationConfig)
        database_config: DatabaseConfig = IocManager.config_manager.get(DatabaseConfig)
        IocManager.config_manager.set(DatabaseConfig, "application_name", application_config.name)
        config_value = IocManager.config_manager.get(DatabaseConfig)
        injector_value = IocManager.injector.get(DatabaseConfig)
        assert config_value.application_name is not None
        assert config_value.application_name == database_config.application_name
        assert config_value.application_name == injector_value.application_name

    def test_RepositoryFactory(self):

        data_operation_repository = RepositoryProvider().get(DataOperation)
        operation = data_operation_repository.filter_by(IsDeleted=0).all()
        assert operation is not None

    def test_folders1(self):
        indexer = ':{index}'
        st = indexer.format(index=5)
        assert st == ':5'
        indexer = '%s'
        st = indexer.format(index=5)
        assert st == '%s'
        indexer = '?'
        st = indexer.format(index=5)
        assert st == '?'
        folders = Utils.find_sub_folders(self.root_directory + '\\models\\dao')
        module_list, module_attr_list = Utils.get_modules(folders)
        for module in module_list:
            print(module)

    def test_datetime_encode(self):
        class DateTimeEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, datetime.datetime):
                    encoded_object = obj.isoformat()
                else:
                    encoded_object = json.JSONEncoder.default(self, obj)
                return encoded_object

        sample = {}
        sample['title'] = "String"
        sample['somedate'] = datetime.datetime.now()


        print(json.dumps(sample, cls=DateTimeEncoder))

    def test_start_operation(self):
        start = time()
        from domain.operation.execution.services.OperationExecution import OperationExecution
        from domain.operation.commands.CreateExecutionCommand import CreateExecutionCommand
        data_operation_id=205
        job_id=680
        execution_id = IocManager.injector.get(CreateExecutionCommand).execute(data_operation_id=data_operation_id, job_id=job_id)
        operation_execution: OperationExecution = IocManager.injector.get(OperationExecution)
        result = operation_execution.start(data_operation_id=data_operation_id, job_id=job_id,
                                           data_operation_job_execution_id=execution_id)

        print(result)
        end = time()
        print(f"EndTime :{end}")
        print(f"TotalTime :{end - start}")
