import os
import traceback
from time import time
from injector import inject

from domain.operation.adapters.ExecuteAdapter import ExecuteAdapter
from domain.operation.adapters.ExecuteAdapterFactory import ExecuteAdapterFactory
from domain.operation.services.DataOperationIntegrationService import DataOperationIntegrationService
from domain.operation.services.DataOperationJobExecutionService import DataOperationJobExecutionService
from domain.operation.services.DataOperationJobService import DataOperationJobService
from domain.operation.services.DataOperationService import DataOperationService
from infrastructor.IocManager import IocManager
from infrastructor.data.decorators.TransactionHandler import transaction_handler
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
from infrastructor.multi_processing.ParallelMultiProcessing import TaskData
from models.enums.StatusTypes import StatusTypes
from models.enums.events import EVENT_EXECUTION_STARTED, EVENT_EXECUTION_FINISHED


class OperationExecutor(IScoped):
    @inject
    def __init__(self,
                 sql_logger: SqlLogger,

                 data_operation_service: DataOperationService,
                 data_operation_integration_service: DataOperationIntegrationService,
                 data_operation_job_service: DataOperationJobService,
                 data_operation_job_execution_service: DataOperationJobExecutionService,
                 execute_adapter_factory: ExecuteAdapterFactory):
        self.data_operation_integration_service = data_operation_integration_service
        self.data_operation_job_service = data_operation_job_service
        self.data_operation_job_execution_service = data_operation_job_execution_service
        self.execute_adapter_factory = execute_adapter_factory
        self.data_operation_service = data_operation_service
        self.sql_logger = sql_logger

    @transaction_handler
    def __start_execution(self, data_operation_id: int, data_operation_job_execution_id: int):
        data_operation_integrations = self.data_operation_integration_service.get_all_by_data_operation_id(
            data_operation_id=data_operation_id).order_by("Order").all()
        if data_operation_integrations is None or len(data_operation_integrations) == 0:
            self.sql_logger.info('Data operation has no data_integration ', job_id=data_operation_job_execution_id)
            return None

        for data_operation_integration in data_operation_integrations:
            execute_adapter: ExecuteAdapter = self.execute_adapter_factory.get_execute_adapter(
                data_operation_integration.DataIntegrationId)
            execute_adapter.start_execute(data_operation_job_execution_id=data_operation_job_execution_id,
                                          data_operation_integration_id=data_operation_integration.Id)

    @transaction_handler
    def start(self, data_operation_id: int, job_id: int):

        self.__check(data_operation_id=data_operation_id, job_id=job_id)
        data_operation_job_execution = self.__create(data_operation_id=data_operation_id,
                                                     job_id=job_id)
        data_operation_job_execution_id = data_operation_job_execution.Id
        data_operation_name = self.data_operation_service.get_name(id=data_operation_id)
        try:

            self.__event(data_operation_job_execution_id=data_operation_job_execution_id,
                         log=f'{data_operation_name} data operation is begin',
                         status=StatusTypes.Start,
                         event_code=EVENT_EXECUTION_STARTED)
            self.__start_execution(data_operation_id=data_operation_id,
                                   data_operation_job_execution_id=data_operation_job_execution_id)
            self.__event(data_operation_job_execution_id=data_operation_job_execution_id,
                         log=f'{data_operation_name} data operation is completed',
                         status=StatusTypes.Finish,
                         event_code=EVENT_EXECUTION_FINISHED,
                         is_finished=True)

            return "Operation Completed"
        except Exception as ex:
            self.__event(data_operation_job_execution_id=data_operation_job_execution_id,
                         log=f'{data_operation_name} data operation has error. Error: {ex}',
                         status=StatusTypes.Error,
                         event_code=EVENT_EXECUTION_FINISHED,
                         is_finished=True)
            raise

    def __check(self, data_operation_id: int, job_id: int):
        data_operation = self.data_operation_service.get_by_id(id=data_operation_id)
        if data_operation is None:
            self.sql_logger.info('Data operation not founded')
            return None

        data_operation_job = self.data_operation_job_service.get_by_operation_and_job_id(
            data_operation_id=data_operation_id,
            job_id=job_id)
        if data_operation_job is None:
            self.sql_logger.info('Data operation job not founded')
            return None

    def __create(self, data_operation_id: int, job_id: int):
        data_operation_job = self.data_operation_job_service.get_by_operation_and_job_id(
            data_operation_id=data_operation_id,
            job_id=job_id)
        data_operation_job_execution = self.data_operation_job_execution_service.create(
            data_operation_job=data_operation_job)
        return data_operation_job_execution

    def __event(self, data_operation_job_execution_id, log: str, status: StatusTypes, event_code: int,
                is_finished: bool = False):
        self.sql_logger.info(log,
                             job_id=data_operation_job_execution_id)
        self.data_operation_job_execution_service.update_status(
            data_operation_job_execution_id=data_operation_job_execution_id,
            status_id=status.value, is_finished=is_finished)
        self.data_operation_job_execution_service.create_event(
            data_operation_execution_id=data_operation_job_execution_id,
            event_code=event_code)
        if is_finished:
            self.data_operation_job_execution_service.send_data_operation_finish_mail(data_operation_job_execution_id)

    def job_start_operation(self, data_operation_id, job_id, sub_process_id, process_name, tasks, results):

        try:
            print('[%s] evaluation routine starts' % process_name)

            while True:
                # waiting for new task
                new_task: TaskData = tasks.get()
                new_task.SubProcessId = sub_process_id
                start = time()
                self.sql_logger.info(
                    f"{job_id}-{data_operation_id} process started.")

                result = self.start(data_operation_id=data_operation_id, job_id=job_id)
                end = time()
                self.sql_logger.info(
                    f"{job_id}-{data_operation_id} process finished. time:{end - start}")
                new_task.IsProcessed = True
                new_task.IsFinished = True
                new_task.Data.State = 1
                new_task.Data.Result = result
                results.put(new_task)
        except Exception as ex:
            self.sql_logger.error(f"{job_id}-{data_operation_id} process getting error:{ex}", job_id=job_id)
            data = new_task.Data
            data.State = 2
            data.Message = str(ex)
            data.Exception = ex
            data.Traceback = traceback.format_exc()
            data = TaskData(Data=data, SubProcessId=sub_process_id, IsFinished=True)
            results.put(data)

    @staticmethod
    def job_start_thread(process_id, job_id, sub_process_id, process_name, tasks, results):
        root_directory = os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, os.pardir))
        IocManager.configure_startup(root_directory)
        operation_executor = IocManager.injector.get(OperationExecutor)
        operation_executor.job_start_operation(data_operation_id=process_id, job_id=job_id,
                                               sub_process_id=sub_process_id, process_name=process_name,
                                               tasks=tasks, results=results)
