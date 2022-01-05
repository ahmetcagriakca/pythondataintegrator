from injector import inject
from pdip.cqrs import Dispatcher
from pdip.cqrs import ICommandHandler
from pdip.data.repository import RepositoryProvider

from pdi.application.job.services.JobOperationService import JobOperationService
from pdi.application.operation.services.DataOperationJobService import DataOperationJobService
from pdi.application.schedule.DeleteCronJob.DeleteCronJobCommand import DeleteCronJobCommand
from pdi.application.schedule.DeleteCronJob.DeleteCronJobRequest import DeleteCronJobRequest
from pdi.application.schedule.RescheduleCronJob.RescheduleCronJobCommand import RescheduleCronJobCommand
from pdi.application.schedule.ScheduleCronJob.ScheduleCronJobCommand import ScheduleCronJobCommand
from pdi.application.schedule.ScheduleCronJob.ScheduleCronJobRequest import ScheduleCronJobRequest


class RescheduleCronJobCommandHandler(ICommandHandler[RescheduleCronJobCommand]):
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

    def handle(self, command: RescheduleCronJobCommand):
        all_cron_jobs = self.data_operation_job_service.get_all_cron_jobs_by_data_operation_name(
            data_operation_name=command.request.DataOperationName).all()
        if all_cron_jobs is not None and len(all_cron_jobs) > 0:
            for cron_job in all_cron_jobs:
                self.delete_exiting_cron_jobs(operation_name=cron_job.DataOperation.Name)
            cron_job = all_cron_jobs[0].DataOperationJob
            self.reschedule_job(cron_job=cron_job)

    def reschedule_job(self, cron_job):
        if cron_job.DataOperation.IsDeleted == 0:
            req = ScheduleCronJobRequest(
                OperationName=cron_job.DataOperation.Name,
                Cron=cron_job.Cron,
                StartDate=cron_job.StartDate,
                EndDate=cron_job.EndDate)
            command = ScheduleCronJobCommand(request=req)
            self.dispatcher.dispatch(command)

    def delete_exiting_cron_jobs(self, operation_name: str):
        req = DeleteCronJobRequest(OperationName=operation_name)
        command = DeleteCronJobCommand(request=req)
        self.dispatcher.dispatch(command)
