from injector import inject
from domain.schedule.DeleteCronJob.DeleteCronJobCommand import DeleteCronJobCommand
from infrastructure.cqrs.ICommandHandler import ICommandHandler


class DeleteCronJobCommandHandler(ICommandHandler[DeleteCronJobCommand]):
    @inject
    def __init__(self,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass
        
    def handle(self, command: DeleteCronJobCommand):
        self.job_operation_service.delete_scheduler_cron_job(data_operation_name=command.DataOperationName)
