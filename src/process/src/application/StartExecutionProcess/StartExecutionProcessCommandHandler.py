import multiprocessing
import os
import subprocess
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
from pdip.integrator.connection.domain.enums import ConnectionTypes
from pdip.logging.loggers.sql import SqlLogger

from src.application.StartExecutionProcess.StartExecutionProcessCommand import StartExecutionProcessCommand
from src.application.integrator.converters.OperationConverter import OperationConverter
from src.domain.aps import ApSchedulerJob, ApSchedulerEvent, ApSchedulerJobEvent
from src.domain.operation import DataOperation, DataOperationJob


class StartExecutionProcessCommandHandler(ICommandHandler[StartExecutionProcessCommand]):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 logger: SqlLogger,
                 integrator: Integrator,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.integrator = integrator
        self.logger = logger
        self.dispatcher = dispatcher

    def handle(self, command: StartExecutionProcessCommand):
        """
        :param job_id: Ap Scheduler Job Id
        :param data_operation_id: Data Operation Id
        :return:
        """
        default_message = f'{command.DataOperationId}-{command.JobId}'
        try:
            start = time.time()
            start_datetime = datetime.now()
            application_config = DependencyContainer.Instance.get(ApplicationConfig)

            data_operation_name = self.get_data_operation_name(data_operation_id=command.DataOperationId)
            default_message += f'-{data_operation_name}'
            self.logger.info(
                f"{default_message} Execution Create started",
                job_id=command.DataOperationJobExecutionId)

            manager = multiprocessing.Manager()
            process_queue = manager.Queue()
            operation_process = Process(target=self.start_process,
                                        args=(application_config.root_directory,
                                              command.DataOperationId, command.JobId,
                                              command.DataOperationJobExecutionId,
                                              process_queue))
            operation_process.start()
            max_check_count = 30
            check_count = 0
            while True:
                check_count += 1
                operation_process.join(timeout=1)
                if operation_process.is_alive():
                    result = process_queue.get(timeout=60)
                    self.logger.info(
                        f"{default_message} Execution running on {operation_process.pid}. Process Message:{result}",
                        job_id=command.DataOperationJobExecutionId)
                    process_queue.task_done()
                    break
                else:
                    if check_count > max_check_count:
                        break
            end_datetime = datetime.now()
            end = time.time()
            self.logger.info(
                f"{default_message} Execution Create finished. Start :{start_datetime} - End :{end_datetime} - ElapsedTime :{end - start}",
                job_id=command.DataOperationJobExecutionId)
            if command.WaitToFinish:
                operation_process.join()
        except Exception as ex:
            self.logger.exception(ex,
                                  f"{default_message} Execution Create getting error. ",
                                  job_id=command.DataOperationJobExecutionId)
            raise
        finally:
            if manager is not None:
                manager.shutdown()

    @transactionhandler
    def get_data_operation_name(self, data_operation_id):
        repository_provider = DependencyContainer.Instance.get(RepositoryProvider)
        data_operation = repository_provider.get(DataOperation).first(Id=data_operation_id)
        if data_operation is None:
            raise Exception('Operation Not Found')
        return data_operation.Name

    @staticmethod
    def start_process(
            root_directory: str,
            data_operation_id: int,
            job_id: int,
            data_operation_job_execution_id: int,
            process_queue: Queue
    ):
        pdi = Pdi(
            root_directory=root_directory,
            initialize_flask=False
        )
        pdi.get(StartExecutionProcessCommandHandler).start(
            data_operation_id=data_operation_id,
            job_id=job_id,
            data_operation_job_execution_id=data_operation_job_execution_id,
            process_queue=process_queue
        )

    def check_removed_job(
            self,
            ap_scheduler_job_id
    ):
        EVENT_JOB_REMOVED = 2 ** 10
        repository_provider = DependencyContainer.Instance.get(RepositoryProvider)
        job_detail_query = repository_provider.query(
            ApSchedulerJob, ApSchedulerEvent, ApSchedulerJobEvent
        ) \
            .filter(ApSchedulerJobEvent.ApSchedulerJobId == ApSchedulerJob.Id) \
            .filter(ApSchedulerJobEvent.EventId == ApSchedulerEvent.Id) \
            .filter(ApSchedulerEvent.Code == EVENT_JOB_REMOVED) \
            .filter(ApSchedulerJob.Id == ap_scheduler_job_id)
        job_detail = job_detail_query.first()
        if job_detail is not None:
            data_operation_job = repository_provider.get(
                DataOperationJob).first(IsDeleted=0,
                                        ApSchedulerJobId=job_detail.ApSchedulerJob.Id)
            if data_operation_job is not None:
                repository_provider.get(DataOperationJob).delete_by_id(data_operation_job.Id)
        DependencyContainer.Instance.get(RepositoryProvider).commit()

    @transactionhandler
    def start(
            self,
            data_operation_id: int,
            job_id: int,
            data_operation_job_execution_id: int,
            process_queue: Queue
    ):
        process_queue.put(f'{os.getppid()} initialized {current_process().name}({os.getpid()}) process')
        start = time.time()
        start_datetime = datetime.now()

        self.logger.info(f"{data_operation_id}-{job_id} Data Operations Started",
                         job_id=data_operation_job_execution_id)
        try:

            operation_converter = DependencyContainer.Instance.get(OperationConverter)
            operation = operation_converter.convert(data_operation_id=data_operation_id)
            for operation_integration in operation.Integrations:
                if operation_integration.Integration.SourceConnections is not None and \
                        operation_integration.Integration.SourceConnections.ConnectionType is not None and \
                        operation_integration.Integration.SourceConnections.ConnectionType == ConnectionTypes.BigData and \
                        operation_integration.Integration.SourceConnections.ConnectionType.BigData is not None:
                    connection_config = operation_integration.Integration.SourceConnections.BigData.Connection
                    username = connection_config.KerberosAuthentication.Principal
                    realm = connection_config.KerberosAuthentication.KrbRealm
                    password = connection_config.KerberosAuthentication.Password
                    success = subprocess.run(['kinit', '%s@%s' % (username, realm)], input=password.encode(),
                                             stdout=subprocess.DEVNULL,
                                             stderr=subprocess.DEVNULL).returncode
                    ret_val = not bool(success)
                    break
            integrator = DependencyContainer.Instance.get(Integrator)
            integrator.integrate(operation, execution_id=data_operation_job_execution_id, ap_scheduler_job_id=job_id)
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
