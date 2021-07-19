from injector import inject
from domain.schedule.ScheduleCronJob.ScheduleCronJobCommand import ScheduleCronJobCommand
from infrastructure.cqrs.ICommandHandler import ICommandHandler


class ScheduleCronJobCommandHandler(ICommandHandler[ScheduleCronJobCommand]):
    @inject
    def __init__(self,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def handle(self, command: ScheduleCronJobCommand):
        self.job_operation_service.create_job_with_cron(operation_name=command.request.OperationName,
                                                        cron=command.request.Cron,
                                                        start_date=command.request.StartDate,
                                                        end_date=command.request.EndDate)
