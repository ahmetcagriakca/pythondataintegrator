from injector import inject

from domain.job.services.JobOperationService import JobOperationService
from domain.notification.SendNotification.SendNotificationCommand import SendNotificationCommand
from domain.notification.SendNotification.SendNotificationRequest import NotificationAdditionalData, \
    SendNotificationRequest
from domain.schedule.DeleteCronJob.DeleteCronJobCommand import DeleteCronJobCommand
from domain.schedule.DeleteCronJob.DeleteCronJobRequest import DeleteCronJobRequest
from domain.schedule.ScheduleCronJob.ScheduleCronJobCommand import ScheduleCronJobCommand
from pdip.cqrs import Dispatcher
from pdip.cqrs import ICommandHandler
from pdip.data import RepositoryProvider


class ScheduleCronJobCommandHandler(ICommandHandler[ScheduleCronJobCommand]):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 repository_provider: RepositoryProvider,
                 job_operation_service: JobOperationService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher
        self.repository_provider = repository_provider
        self.job_operation_service = job_operation_service

    def handle(self, command: ScheduleCronJobCommand):
        cron_job_exist=self.job_operation_service.check_cron_initialized_jobs_by_data_operation_name(
                data_operation_name=command.request.OperationName)
        if cron_job_exist:
            self.delete_exiting_cron_jobs(operation_name=command.request.OperationName)

        data_operation_job = self.job_operation_service.create_job_with_cron(
            operation_name=command.request.OperationName,
            cron=command.request.Cron,
            start_date=command.request.StartDate,
            end_date=command.request.EndDate)
        self.repository_provider.commit()

        self.notify(id=data_operation_job.Id, name=data_operation_job.DataOperation.Name)

    def delete_exiting_cron_jobs(self, operation_name: str):
        req = DeleteCronJobRequest(OperationName=operation_name)
        command = DeleteCronJobCommand(request=req)
        self.dispatcher.dispatch(command)

    def notify(self, id: int, name: str):
        data_list = []
        data = NotificationAdditionalData(Key="Type", Value="DataOperationJob")
        data_list.append(data)
        data = NotificationAdditionalData(Key="Id", Value=id)
        data_list.append(data)
        data = NotificationAdditionalData(Key="Name", Value=name)
        data_list.append(data)
        message = f"{name} operation, job {id} created"

        send_notification_request = SendNotificationRequest(Message=message, Type=1, Action=1,
                                                            AdditionalData=data_list)
        self.dispatcher.dispatch(SendNotificationCommand(request=send_notification_request))
