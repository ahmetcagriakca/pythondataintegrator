from injector import inject

from domain.job.services.JobOperationService import JobOperationService
from domain.schedule.ScheduleJob.ScheduleJobCommand import ScheduleJobCommand
from infrastructure.cqrs.ICommandHandler import ICommandHandler


class ScheduleJobCommandHandler(ICommandHandler[ScheduleJobCommand]):
    @inject
    def __init__(self,
                 job_operation_service: JobOperationService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job_operation_service = job_operation_service

    def handle(self, command: ScheduleJobCommand):
        self.job_operation_service.insert_job_with_date(operation_name=command.request.OperationName,
                                                        run_date=command.request.RunDate)
