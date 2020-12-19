from datetime import datetime
from time import time
from unittest import TestCase

import os

from infrastructor.IocManager import IocManager

from models.configs.ApiConfig import ApiConfig

from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.logging.ConsoleLogger import ConsoleLogger
from infrastructor.logging.SqlLogger import SqlLogger
from infrastructor.multi_processing.ParallelMultiProcessing import TaskData, ParallelMultiProcessing


class TestMultiProcess(TestCase):

    def __init__(self, methodName='runProcessTest'):
        super(TestMultiProcess, self).__init__(methodName)

        from infrastructor.api.FlaskAppWrapper import FlaskAppWrapper
        from infrastructor.scheduler.JobScheduler import JobScheduler
        os.environ["PYTHON_ENVIRONMENT"] = 'test'
        root_directory = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))
        IocManager.configure_startup(root_directory=root_directory,
                                     app_wrapper=FlaskAppWrapper,
                                     job_scheduler=JobScheduler)
        self.client = IocManager.app.test_client()

    def print_error_detail(self, data):
        print(data['message'] if 'message' in data else '')
        print(data['traceback'] if 'traceback' in data else '')
        print(data['message'] if 'message' in data else '')

    @staticmethod
    def calculate_method(sql_logger, process_name, my_value):
        sql_logger.info(f"{process_name} process worked with {my_value}")
        # Compute result and mimic a long-running task
        compute = my_value * my_value
        # Output which process received the value
        # and the calculation result
        print('[%s] received value: %i' % (process_name, my_value))
        print('[%s] calculated value: %i' % (process_name, compute))
        # Add result to the queue
        sql_logger.info(f"{process_name} process calculated {compute}")
        return compute

    @staticmethod
    def parallel_data_test(process_name, tasks, results):

        print('[%s] evaluation routine starts' % process_name)
        api_config = IocManager.config_manager.get(ApiConfig)
        console_logger = IocManager.config_manager.get(ConsoleLogger)
        database_session_manager = DatabaseSessionManager(database_config=database_config, api_config=api_config,
                                                          console_logger=console_logger)
        # database_session_manager = IocManager.config_manager.get(DatabaseSessionManager)
        sql_logger = SqlLogger(api_config=api_config, console_logger=console_logger,
                               database_session_manager=database_session_manager)
        while True:
            new_value = tasks.get()
            if new_value.IsFinished:
                sql_logger.info(f"{process_name} process finished")
                print('[%s] evaluation routine quits' % process_name)
                # Indicate finished
                results.put(new_value)
                break
            else:
                new_value.Data.Result = TestMultiProcess.calculate_method(sql_logger, process_name,
                                                                          new_value.Data.Value)
                # Add result to the queue
                results.put(new_value)

    @staticmethod
    def parallel_test_result(result: TaskData):
        if not result.IsFinished:
            print(f'value {result.Data.Value} result:{result.Data.Result}')

    def test_performance_parallel(self):

        start = time()
        print(f"StartTime :{start}")
        from domain.pdi.services.TestParallelService import TestParallelService, TaskValue
        test_parallel_service: TestParallelService = IocManager.injector.get(TestParallelService)
        result = test_parallel_service.test_performance_parallel(1000)
        print(result)
        end = time()
        print(f"EndTime :{end}")
        print(f"TotalTime :{end - start}")

    def test_parallel(self):

        from domain.pdi.services.TestParallelService import TaskValue
        start = time()
        print(f"StartTime :{start}")
        start_datetime = datetime.now()

        sql_logger = IocManager.injector.get(SqlLogger)
        sql_logger.info(f"MultiThread Operations Started")
        parallel_multi_processing = ParallelMultiProcessing(10)
        parallel_multi_processing.configure_process()
        parallel_multi_processing.start_processes(TestMultiProcess.parallel_data_test)
        for i in range(100):
            tv = TaskValue(i)
            td = TaskData(tv)
            parallel_multi_processing.add_task(td)
        parallel_multi_processing.finish_tasks()
        parallel_multi_processing.check_processes(TestMultiProcess.parallel_test_result)
        end_datetime = datetime.now()
        end = time()
        print(f"Start :{start_datetime}")
        print(f"End :{end_datetime}")
        print(f"ElapsedTime :{end - start}")
        return start_datetime, end_datetime, start, end

    def test_with_not_parallel(self):

        from domain.pdi.services.TestParallelService import TaskValue
        start = time()
        print(f"StartTime :{start}")
        start_datetime = datetime.now()
        sql_logger = IocManager.injector.get(SqlLogger)
        sql_logger.info(f"One Thread Operations Started")
        for i in range(100):
            tv = TaskValue(i)
            td = TaskData(tv)
            td.Data.Result = TestMultiProcess.calculate_method(sql_logger, "MainProcess", td.Data.Value)
            TestMultiProcess.parallel_test_result(td)
        end_datetime = datetime.now()
        end = time()
        print(f"Start :{start_datetime}")
        print(f"End :{end_datetime}")
        print(f"ElapsedTime :{end - start}")
        return start_datetime, end_datetime, start, end
