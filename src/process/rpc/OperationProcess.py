import time
import traceback

from IocManager import IocManager

from datetime import datetime
from domain.operation.execution.services.OperationExecution import OperationExecution
from domain.operation.services.DataOperationJobService import DataOperationJobService
from infrastructor.data.RepositoryProvider import RepositoryProvider
from infrastructor.data.decorators.TransactionHandler import transaction_handler
from infrastructor.logging.SqlLogger import SqlLogger

from multiprocessing.context import Process

from models.dao.operation import DataOperation


class OperationProcess:
    @transaction_handler
    def start(self, data_operation_id: int, job_id: int, data_operation_job_execution_id: int):
        start = time.time()
        start_datetime = datetime.now()

        sql_logger = SqlLogger()
        sql_logger.info(f"{data_operation_id}-{job_id} Data Operations Started",
                        job_id=data_operation_job_execution_id)
        try:
            IocManager.injector.get(OperationExecution).start(data_operation_id=data_operation_id, job_id=job_id,
                                                              data_operation_job_execution_id=data_operation_job_execution_id)
            sql_logger.info(
                f"{data_operation_id}-{job_id} Data Operations Finished",
                job_id=data_operation_job_execution_id)
        except Exception as ex:
            exc = traceback.format_exc() + '\n' + str(ex)
            sql_logger.info(
                f"{data_operation_id}-{job_id} Data Operations Finished With Error: {exc}",
                job_id=data_operation_job_execution_id)
        finally:
            IocManager.injector.get(DataOperationJobService).check_removed_job(ap_scheduler_job_id=job_id)

        end_datetime = datetime.now()
        end = time.time()
        sql_logger.info(
            f"{data_operation_id}-{job_id} Start :{start_datetime} - End :{end_datetime} - ElapsedTime :{end - start}",

            job_id=data_operation_job_execution_id)
        del sql_logger

    @staticmethod
    def start_process(data_operation_id: int, job_id: int, data_operation_job_execution_id: int):
        IocManager.initialize()
        operation_process = OperationProcess()
        operation_process.start(data_operation_id=data_operation_id, job_id=job_id,
                                data_operation_job_execution_id=data_operation_job_execution_id)
        del operation_process

    @transaction_handler
    def start_operation_process(self, data_operation_id: int, job_id: int, data_operation_job_execution_id: int):
        """
        :param job_id: Ap Scheduler Job Id
        :param data_operation_id: Data Operation Id
        :return:
        """
        start = time.time()
        start_datetime = datetime.now()

        sql_logger = SqlLogger()
        data_operation_query = IocManager.injector.get(RepositoryProvider).get(DataOperation).filter_by(
            Id=data_operation_id)
        data_operation = data_operation_query.first()
        if data_operation is None:
            raise Exception('Operation Not Found')

        sql_logger.info(f"{data_operation_id}-{job_id}-{data_operation.Name} Execution Create started",
                        job_id=data_operation_job_execution_id)
        operation_process = Process(target=OperationProcess.start_process,
                                    args=(data_operation_id, job_id, data_operation_job_execution_id))
        operation_process.start()
        #check process start
        # time.sleep(1)
        while True:
            operation_process.join(timeout=1)
            if operation_process.is_alive():
                sql_logger.info(f"{data_operation_id}-{job_id}-{data_operation.Name} Execution running on {operation_process.pid}",
                        job_id=data_operation_job_execution_id)
                break
            
            time.sleep(1)

        end_datetime = datetime.now()
        end = time.time()
        sql_logger.info(
            f"{data_operation_id}-{job_id}-{data_operation.Name} Execution Create finished. Start :{start_datetime} - End :{end_datetime} - ElapsedTime :{end - start}",
            job_id=data_operation_job_execution_id)
        IocManager.injector.get(RepositoryProvider).close()
        return
