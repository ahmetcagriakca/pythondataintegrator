from injector import inject

from domain.job.services.JobOperationService import JobOperationService
from domain.notification.SendNotification.SendNotificationCommand import SendNotificationCommand
from domain.notification.SendNotification.SendNotificationRequest import NotificationAdditionalData, \
    SendNotificationRequest
from domain.schedule.DeleteCronJob.DeleteCronJobCommand import DeleteCronJobCommand
from infrastructure.cqrs.Dispatcher import Dispatcher
from infrastructure.cqrs.ICommandHandler import ICommandHandler
from infrastructure.data.RepositoryProvider import RepositoryProvider


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
                message=f'{data_operation_job.DataOperation.Name} operation, job {data_operation_job.Id} removed',
                id=data_operation_job.Id)

    def notify(self, message: str, id: int):
        data_list = []
        data = NotificationAdditionalData(Key="Type", Value="DataOperationJob")
        data_list.append(data)
        data = NotificationAdditionalData(Key="Id", Value=id)
        data_list.append(data)
        send_notification_request = SendNotificationRequest(Message=message, Type=1, Action=3, AdditionalData=data_list)
        self.dispatcher.dispatch(SendNotificationCommand(request=send_notification_request))