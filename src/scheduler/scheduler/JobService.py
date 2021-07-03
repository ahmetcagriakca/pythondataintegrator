from IocManager import IocManager
from domain.operation.commands.CreateExecutionCommand import CreateExecutionCommand
from domain.operation.commands.SendSchedulerErrorMailCommand import SendSchedulerErrorMailCommand
from infrastructor.data.decorators.TransactionHandler import transaction_handler
from infrastructor.logging.SqlLogger import SqlLogger
import time
from datetime import datetime
from rpc.ProcessRpcClientService import ProcessRpcClientService


class JobService:
    @transaction_handler
    def start_data_operation(self, job_id, data_operation_id: int):
        """
        :param job_id: Ap Scheduler Job Id
        :param data_operation_id: Data Operation Id
        :return:
        """
        data_operation_job_execution_id = None
        sql_logger = SqlLogger()
        try:
            start = time.time()
            start_datetime = datetime.now()

            command = CreateExecutionCommand()
            data_operation_job_execution_id = command.execute(data_operation_id=data_operation_id,
                                                                            job_id=job_id)
            del command
            sql_logger.info(f"{data_operation_id}-{job_id} Scheduler Started ", job_id=data_operation_job_execution_id)
            sql_logger.info(
                f"{data_operation_id}-{job_id} Scheduler execution created ",
                job_id=data_operation_job_execution_id)
            IocManager.injector.get(ProcessRpcClientService).call_job_start(data_operation_id=data_operation_id,
                                                                            job_id=job_id,
                                                                            data_operation_job_execution_id=data_operation_job_execution_id)
            end_datetime = datetime.now()
            end = time.time()
            sql_logger.info(
                f"{data_operation_id}-{job_id} Scheduler Finished. Start :{start_datetime}-End :{end_datetime}-ElapsedTime :{end - start}",
                job_id=data_operation_job_execution_id)
        except Exception as ex:
            command = SendSchedulerErrorMailCommand()
            command.send(job_id=job_id, exception=ex,
                         data_operation_job_execution_id=data_operation_job_execution_id)
            del command
            sql_logger.info(
                f"{data_operation_id}-{job_id} Scheduler getting error. Error:{ex}",
                job_id=data_operation_job_execution_id)
            raise
        finally:
            del sql_logger

    @staticmethod
    def job_start_data_operation(job_id, data_operation_id: int):
        job_service = JobService()
        job_service.start_data_operation(job_id=job_id, data_operation_id=data_operation_id)
        del job_service
