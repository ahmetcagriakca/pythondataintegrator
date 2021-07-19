from injector import inject

from domain.job.services.JobOperationService import JobOperationService
from domain.schedule.DeleteJob.DeleteJobCommand import DeleteJobCommand
from infrastructure.cqrs.ICommandHandler import ICommandHandler


class DeleteJobCommandHandler(ICommandHandler[DeleteJobCommand]):
    @inject
    def __init__(self,
                 job_operation_service: JobOperationService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job_operation_service = job_operation_service

    def handle(self, command: DeleteJobCommand):
        self.job_operation_service.delete_scheduler_date_job(
            data_operation_job_id=command.Id)
