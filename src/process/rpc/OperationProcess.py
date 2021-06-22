import time
import traceback

from IocManager import IocManager

from datetime import datetime
from domain.operation.execution.services.OperationExecution import OperationExecution
from domain.operation.services.DataOperationJobService import DataOperationJobService
from infrastructor.logging.SqlLogger import SqlLogger

from multiprocessing.context import Process


class OperationProcess:

    @staticmethod
    def start_operation(data_operation_id: int, job_id: int):
        IocManager.initialize()
        start = time.time()
        start_datetime = datetime.now()

        sql_logger = SqlLogger()
        sql_logger.info(f"{job_id}-{data_operation_id} Data Operations Started")
        try:
            IocManager.injector.get(OperationExecution).start(data_operation_id=data_operation_id, job_id=job_id)
            sql_logger.info(f"{job_id}-{data_operation_id} Data Operations Finished")
        except Exception as ex:
            exc = traceback.format_exc() + '\n' + str(ex)
            sql_logger.info(f"{job_id}-{data_operation_id} Data Operations Finished With Error: {exc}")
        finally:
            IocManager.injector.get(DataOperationJobService).check_removed_job(ap_scheduler_job_id=job_id)

        end_datetime = datetime.now()
        end = time.time()
        sql_logger.info(f"{job_id}-{data_operation_id} Start :{start_datetime}")
        sql_logger.info(f"{job_id}-{data_operation_id} End :{end_datetime}")
        sql_logger.info(f"{job_id}-{data_operation_id} ElapsedTime :{end - start}")
        del sql_logger

    @staticmethod
    def start_operation_process(job_id, data_operation_id: int):
        """
        :param job_id: Ap Scheduler Job Id
        :param data_operation_id: Data Operation Id
        :return:
        """
        start = time.time()
        start_datetime = datetime.now()

        sql_logger = SqlLogger()
        sql_logger.info(f"{job_id}-{data_operation_id} Execution Create started")
        operation_process = Process(target=OperationProcess.start_operation, args=(data_operation_id, job_id))
        operation_process.start()
        end_datetime = datetime.now()
        end = time.time()
        sql_logger.info(
            f"{job_id}-{data_operation_id} Execution Create finished. Start :{start_datetime} - End :{end_datetime} - ElapsedTime :{end - start}")
