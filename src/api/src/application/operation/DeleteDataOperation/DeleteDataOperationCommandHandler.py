from injector import inject
from pdip.cqrs import Dispatcher
from pdip.cqrs import ICommandHandler
from pdip.data.repository import RepositoryProvider
from pdip.exceptions import OperationalException

from src.application.notification.SendNotification.SendNotificationCommand import SendNotificationCommand
from src.application.notification.SendNotification.SendNotificationRequest import NotificationAdditionalData, \
    SendNotificationRequest
from src.application.operation.DeleteDataOperation.DeleteDataOperationCommand import DeleteDataOperationCommand
from src.application.operation.services.DataOperationService import DataOperationService
from src.application.schedule.DeleteCronJob.DeleteCronJobCommand import DeleteCronJobCommand
from src.application.schedule.DeleteCronJob.DeleteCronJobRequest import DeleteCronJobRequest


class DeleteDataOperationCommandHandler(ICommandHandler[DeleteDataOperationCommand]):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 repository_provider: RepositoryProvider,
                 data_operation_service: DataOperationService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repository_provider = repository_provider
        self.dispatcher = dispatcher
        self.data_operation_service = data_operation_service

    def handle(self, command: DeleteDataOperationCommand):
        data_operation = self.data_operation_service.get_by_id(id=command.request.Id)
        if data_operation is  None:
            raise OperationalException(f"{command.request.Id} Data Operation not found")
        self.delete_exiting_cron_jobs(operation_name=data_operation.Name)
        result = self.data_operation_service.delete_data_operation(command.request.Id)
        self.repository_provider.commit()
        self.notify(message=result, id=command.request.Id)

    def delete_exiting_cron_jobs(self, operation_name: str):
        req = DeleteCronJobRequest(OperationName=operation_name)
        command = DeleteCronJobCommand(request=req)
        self.dispatcher.dispatch(command)

    def notify(self, message: str, id: int):
        data_list = []
        data = NotificationAdditionalData(Key="Type", Value="DataOperation")
        data_list.append(data)
        data = NotificationAdditionalData(Key="Id", Value=id)
        data_list.append(data)
        send_notification_request = SendNotificationRequest(Message=message, Type=1, Action=3, AdditionalData=data_list)
        self.dispatcher.dispatch(SendNotificationCommand(request=send_notification_request))
