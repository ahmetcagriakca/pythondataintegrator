from injector import inject
from pdip.cqrs import Dispatcher
from pdip.cqrs import ICommandHandler
from pdip.data.repository import RepositoryProvider

from src.application.job.services.JobOperationService import JobOperationService
from src.application.operation.services.DataOperationJobService import DataOperationJobService
from src.application.schedule.RescheduleCronJob.RescheduleCronJobCommand import RescheduleCronJobCommand
from src.application.schedule.RescheduleCronJob.RescheduleCronJobRequest import RescheduleCronJobRequest
from src.application.schedule.RescheduleCronJobs.RescheduleCronJobsCommand import RescheduleCronJobsCommand


class RescheduleCronJobsCommandHandler(ICommandHandler[RescheduleCronJobsCommand]):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 repository_provider: RepositoryProvider,
                 job_operation_service: JobOperationService,
                 data_operation_job_service: DataOperationJobService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_operation_job_service = data_operation_job_service
        self.dispatcher = dispatcher
        self.repository_provider = repository_provider
        self.job_operation_service = job_operation_service

    def handle(self, command: RescheduleCronJobsCommand):
        if command.request.DataOperationNames is not None and len(command.request.DataOperationNames) > 0:
            for data_operation_name in command.request.DataOperationNames:
                req = RescheduleCronJobRequest(DataOperationName=data_operation_name)
                command = RescheduleCronJobCommand(request=req)
                self.dispatcher.dispatch(command)
