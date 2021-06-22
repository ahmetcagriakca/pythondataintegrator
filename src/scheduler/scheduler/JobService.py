import rpyc

from IocManager import IocManager
from infrastructor.logging.SqlLogger import SqlLogger
import time
from datetime import datetime

from rpc.ProcessRpcClientService import ProcessRpcClientService


class JobService:
    @staticmethod
    def job_start_data_operation(job_id, data_operation_id: int):
        """
        :param job_id: Ap Scheduler Job Id
        :param data_operation_id: Data Operation Id
        :return:
        """
        start = time.time()
        start_datetime = datetime.now()

        sql_logger = SqlLogger()
        sql_logger.info(f"{job_id}-{data_operation_id} Data Operations Started")
        """
        TODO: process operations
        """
        IocManager.injector.get(ProcessRpcClientService).job_start(job_id, data_operation_id)
        end_datetime = datetime.now()
        end = time.time()
        sql_logger.info(f"{job_id}-{data_operation_id} Start :{start_datetime}")
        sql_logger.info(f"{job_id}-{data_operation_id} End :{end_datetime}")
        sql_logger.info(f"{job_id}-{data_operation_id} ElapsedTime :{end - start}")