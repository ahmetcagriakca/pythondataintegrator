import multiprocessing
import os
import time
import traceback
from datetime import datetime
from multiprocessing import current_process
from multiprocessing.context import Process
from queue import Queue

from pdip.base import Pdi
from pdip.configuration.models.application import ApplicationConfig
from pdip.data import RepositoryProvider
from pdip.data.decorators import transactionhandler
from pdip.dependency.container import DependencyContainer
from pdip.logging.loggers.database import SqlLogger

from process.domain.aps import ApSchedulerJob, ApSchedulerEvent, ApSchedulerJobEvent
from process.domain.operation import DataOperation, DataOperationJob
from process.application.operation.execution.services.OperationExecution import OperationExecution


class OperationProcess:
    @transactionhandler
    def start(self, data_operation_id: int, job_id: int, data_operation_job_execution_id: int, process_queue: Queue):
        process_queue.put(f'{os.getppid()} initialized {current_process().name}({os.getpid()}) process')
        start = time.time()
        start_datetime = datetime.now()

        logger = DependencyContainer.Instance.get(SqlLogger)
        logger.info(f"{data_operation_id}-{job_id} Data Operations Started",
                    job_id=data_operation_job_execution_id)
        try:
            DependencyContainer.Instance.get(OperationExecution).start(data_operation_id=data_operation_id,
                                                                       job_id=job_id,
                                                                       data_operation_job_execution_id=data_operation_job_execution_id)
            logger.info(
                f"{data_operation_id}-{job_id} Data Operations Finished",
                job_id=data_operation_job_execution_id)
        except Exception as ex:
            exc = traceback.format_exc() + '\n' + str(ex)
            logger.info(
                f"{data_operation_id}-{job_id} Data Operations Finished With Error: {exc}",
                job_id=data_operation_job_execution_id)
        finally:
            def check_removed_job(ap_scheduler_job_id):
                EVENT_JOB_REMOVED = 2 ** 10
                job_detail_query = DependencyContainer.Instance.get(RepositoryProvider).query(
                    ApSchedulerJob, ApSchedulerEvent, ApSchedulerJobEvent
                ) \
                    .filter(ApSchedulerJobEvent.ApSchedulerJobId == ApSchedulerJob.Id) \
                    .filter(ApSchedulerJobEvent.EventId == ApSchedulerEvent.Id) \
                    .filter(ApSchedulerEvent.Code == EVENT_JOB_REMOVED) \
                    .filter(ApSchedulerJob.Id == ap_scheduler_job_id)
                job_detail = job_detail_query.first()
                if job_detail is not None:
                    data_operation_job = DependencyContainer.Instance.get(RepositoryProvider).get(
                        DataOperationJob).first(IsDeleted=0,
                                                ApSchedulerJobId=job_detail.ApSchedulerJob.Id)
                    if data_operation_job is not None:
                        DependencyContainer.Instance.get(RepositoryProvider).get(DataOperationJob).delete_by_id(id)

            check_removed_job(ap_scheduler_job_id=job_id)

        end_datetime = datetime.now()
        end = time.time()
        logger.info(
            f"{data_operation_id}-{job_id} Start :{start_datetime} - End :{end_datetime} - ElapsedTime :{end - start}",

            job_id=data_operation_job_execution_id)
        del logger

    @staticmethod
    def start_process(root_directory: str, data_operation_id: int, job_id: int, data_operation_job_execution_id: int,
                      process_queue: Queue):
        Pdi(root_directory=root_directory, initialize_flask=False)

        operation_process = OperationProcess()
        operation_process.start(data_operation_id=data_operation_id, job_id=job_id,
                                data_operation_job_execution_id=data_operation_job_execution_id,
                                process_queue=process_queue)
        del operation_process

    @transactionhandler
    def start_operation_process(self, data_operation_id: int, job_id: int, data_operation_job_execution_id: int):
        """
        :param job_id: Ap Scheduler Job Id
        :param data_operation_id: Data Operation Id
        :return:
        """
        try:
            start = time.time()
            start_datetime = datetime.now()

            sql_logger = DependencyContainer.Instance.get(SqlLogger)
            application_config = DependencyContainer.Instance.get(ApplicationConfig)
            data_operation_query = DependencyContainer.Instance.get(RepositoryProvider).get(DataOperation).filter_by(
                Id=data_operation_id)
            data_operation = data_operation_query.first()
            if data_operation is None:
                raise Exception('Operation Not Found')

            sql_logger.info(f"{data_operation_id}-{job_id}-{data_operation.Name} Execution Create started",
                            job_id=data_operation_job_execution_id)

            manager = multiprocessing.Manager()
            process_queue = manager.Queue()
            operation_process = Process(target=OperationProcess.start_process,
                                        args=(application_config.root_directory,
                                              data_operation_id, job_id, data_operation_job_execution_id,
                                              process_queue))
            operation_process.start()
            while True:
                operation_process.join(timeout=1)
                if operation_process.is_alive():
                    result = process_queue.get(timeout=60)
                    sql_logger.info(
                        f"{data_operation_id}-{job_id}-{data_operation.Name} Execution running on {operation_process.pid}. Process Message:{result}",
                        job_id=data_operation_job_execution_id)
                    process_queue.task_done()
                    break

            end_datetime = datetime.now()
            end = time.time()
            sql_logger.info(
                f"{data_operation_id}-{job_id}-{data_operation.Name} Execution Create finished. Start :{start_datetime} - End :{end_datetime} - ElapsedTime :{end - start}",
                job_id=data_operation_job_execution_id)
        except Exception as ex:
            exception_traceback = traceback.format_exc()
            sql_logger.info(
                f"{data_operation_id}-{job_id} Execution Create getting error. Error:{ex} traceback:{exception_traceback}",
                job_id=data_operation_job_execution_id)
            raise
        finally:
            if manager is not None:
                manager.shutdown()
