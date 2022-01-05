import multiprocessing
import os
import time
import traceback
from datetime import datetime
from multiprocessing import current_process
from multiprocessing.context import Process
from queue import Queue

from injector import inject
from pdip.base import Pdi
from pdip.configuration.models.application import ApplicationConfig
from pdip.cqrs import Dispatcher, ICommandHandler
from pdip.data.decorators import transactionhandler
from pdip.data.repository import RepositoryProvider
from pdip.dependency.container import DependencyContainer
from pdip.integrator.base import Integrator
from pdip.logging.loggers.sql import SqlLogger

from process.application.StartExecutionProcess.StartExecutionProcessCommand import StartExecutionProcessCommand
from process.application.execution.services.OperationExecution import OperationExecution
from process.application.integrator.OperationConverter import OperationConverter
from process.application.integrator.ProcessIntegratorEventManager import ProcessIntegratorEventManager
from process.domain.aps import ApSchedulerJob, ApSchedulerEvent, ApSchedulerJobEvent
from process.domain.operation import DataOperation, DataOperationJob


class StartExecutionProcessCommandHandler(ICommandHandler[StartExecutionProcessCommand]):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 logger: SqlLogger,
                 repository_provider: RepositoryProvider,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger
        self.repository_provider = repository_provider
        self.dispatcher = dispatcher

    def handle(self, command: StartExecutionProcessCommand):
        """
        :param job_id: Ap Scheduler Job Id
        :param data_operation_id: Data Operation Id
        :return:
        """
        try:
            start = time.time()
            start_datetime = datetime.now()

            application_config = DependencyContainer.Instance.get(ApplicationConfig)
            data_operation_query = DependencyContainer.Instance.get(RepositoryProvider).get(
                DataOperation).filter_by(
                Id=command.DataOperationId)
            data_operation = data_operation_query.first()
            if data_operation is None:
                raise Exception('Operation Not Found')

            self.logger.info(
                f"{command.DataOperationId}-{command.JobId}-{data_operation.Name} Execution Create started",
                job_id=command.DataOperationJobExecutionId)

            manager = multiprocessing.Manager()
            process_queue = manager.Queue()
            operation_process = Process(target=self.start_process,
                                        args=(application_config.root_directory,
                                              command.DataOperationId, command.JobId,
                                              command.DataOperationJobExecutionId,
                                              process_queue))
            operation_process.start()
            while True:
                operation_process.join(timeout=1)
                if operation_process.is_alive():
                    result = process_queue.get(timeout=60)
                    self.logger.info(
                        f"{command.DataOperationId}-{command.JobId}-{data_operation.Name} Execution running on {operation_process.pid}. Process Message:{result}",
                        job_id=command.DataOperationJobExecutionId)
                    process_queue.task_done()
                    break

            end_datetime = datetime.now()
            end = time.time()
            self.logger.info(
                f"{command.DataOperationId}-{command.JobId}-{data_operation.Name} Execution Create finished. Start :{start_datetime} - End :{end_datetime} - ElapsedTime :{end - start}",
                job_id=command.DataOperationJobExecutionId)
            operation_process.join()
        except Exception as ex:
            self.logger.exception(ex,
                                  f"{command.DataOperationId}-{command.JobId} Execution Create getting error. ",
                                  job_id=command.DataOperationJobExecutionId)
            raise
        finally:
            if manager is not None:
                manager.shutdown()

    @staticmethod
    def start_process(root_directory: str, data_operation_id: int, job_id: int,
                      data_operation_job_execution_id: int,
                      process_queue: Queue):
        pdi = Pdi(root_directory=root_directory, initialize_flask=False)
        pdi.get(StartExecutionProcessCommandHandler).start(data_operation_id=data_operation_id, job_id=job_id,
                                                           data_operation_job_execution_id=data_operation_job_execution_id,
                                                           process_queue=process_queue)

    def check_removed_job(self, ap_scheduler_job_id):
        EVENT_JOB_REMOVED = 2 ** 10
        job_detail_query = self.repository_provider.query(
            ApSchedulerJob, ApSchedulerEvent, ApSchedulerJobEvent
        ) \
            .filter(ApSchedulerJobEvent.ApSchedulerJobId == ApSchedulerJob.Id) \
            .filter(ApSchedulerJobEvent.EventId == ApSchedulerEvent.Id) \
            .filter(ApSchedulerEvent.Code == EVENT_JOB_REMOVED) \
            .filter(ApSchedulerJob.Id == ap_scheduler_job_id)
        job_detail = job_detail_query.first()
        if job_detail is not None:
            data_operation_job = self.repository_provider.get(
                DataOperationJob).first(IsDeleted=0,
                                        ApSchedulerJobId=job_detail.ApSchedulerJob.Id)
            if data_operation_job is not None:
                self.repository_provider.get(DataOperationJob).delete_by_id(data_operation_job.Id)

    @transactionhandler
    def start(self, data_operation_id: int, job_id: int, data_operation_job_execution_id: int,
              process_queue: Queue):
        process_queue.put(f'{os.getppid()} initialized {current_process().name}({os.getpid()}) process')
        start = time.time()
        start_datetime = datetime.now()

        self.logger.info(f"{data_operation_id}-{job_id} Data Operations Started",
                         job_id=data_operation_job_execution_id)
        try:

            operation_converter = DependencyContainer.Instance.get(OperationConverter)
            process_integrator_event_manager = DependencyContainer.Instance.get(ProcessIntegratorEventManager)
            operation = operation_converter.convert(data_operation_id=data_operation_id)
            integrator = Integrator(integrator_event_manager=process_integrator_event_manager)
            integrator.integrate(operation, execution_id=data_operation_job_execution_id)
            self.logger.info(
                f"{data_operation_id}-{job_id} Data Operations Finished",
                job_id=data_operation_job_execution_id)
        except Exception as ex:
            exc = traceback.format_exc() + '\n' + str(ex)
            self.logger.info(
                f"{data_operation_id}-{job_id} Data Operations Finished With Error: {exc}",
                job_id=data_operation_job_execution_id)
        finally:
            self.check_removed_job(ap_scheduler_job_id=job_id)

        end_datetime = datetime.now()
        end = time.time()
        self.logger.info(
            f"{data_operation_id}-{job_id} Start :{start_datetime} - End :{end_datetime} - ElapsedTime :{end - start}",

            job_id=data_operation_job_execution_id)
        del self.logger
