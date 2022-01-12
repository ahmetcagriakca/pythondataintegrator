from injector import inject
from pdip.cqrs import Dispatcher
from pdip.cqrs import ICommandHandler
from pdip.data.repository import RepositoryProvider

from src.application.job.services.JobOperationService import JobOperationService
from src.application.notification.SendNotification.SendNotificationCommand import SendNotificationCommand
from src.application.notification.SendNotification.SendNotificationRequest import NotificationAdditionalData, \
    SendNotificationRequest
from src.application.schedule.DeleteCronJob.DeleteCronJobCommand import DeleteCronJobCommand


class DeleteCronJobCommandHandler(ICommandHandler[DeleteCronJobCommand]):
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

    def handle(self, command: DeleteCronJobCommand):
        data_operation_jobs = self.job_operation_service.delete_scheduler_cron_job(
            data_operation_name=command.request.OperationName)
        self.repository_provider.commit()
        for data_operation_job in data_operation_jobs:
            self.notify(
                message=f'{data_operation_job.DataOperation.Name} operation, job {data_operation_job.DataOperationJob.Id} removed',
                id=data_operation_job.DataOperationJob.Id)

    def notify(self, message: str, id: int):
        data_list = []
        data = NotificationAdditionalData(Key="Type", Value="DataOperationJob")
        data_list.append(data)
        data = NotificationAdditionalData(Key="Id", Value=id)
        data_list.append(data)
        send_notification_request = SendNotificationRequest(Message=message, Type=1, Action=3, AdditionalData=data_list)
        self.dispatcher.dispatch(SendNotificationCommand(request=send_notification_request))
