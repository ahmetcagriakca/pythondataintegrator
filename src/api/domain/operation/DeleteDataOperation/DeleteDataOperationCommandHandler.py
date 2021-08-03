from injector import inject

from domain.notification.SendNotification.SendNotificationCommand import SendNotificationCommand
from domain.notification.SendNotification.SendNotificationRequest import NotificationAdditionalData, \
    SendNotificationRequest
from domain.operation.DeleteDataOperation.DeleteDataOperationCommand import DeleteDataOperationCommand
from domain.operation.services.DataOperationService import DataOperationService
from infrastructure.cqrs.Dispatcher import Dispatcher
from infrastructure.cqrs.ICommandHandler import ICommandHandler
from infrastructure.data.RepositoryProvider import RepositoryProvider


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
        result = self.data_operation_service.delete_data_operation(command.request.Id)
        self.repository_provider.commit()
        self.notify(message=result, id=command.request.Id)

    def notify(self, message: str, id: int):
        data_list = []
        data = NotificationAdditionalData(Key="Type", Value="DataOperation")
        data_list.append(data)
        data = NotificationAdditionalData(Key="Id", Value=id)
        data_list.append(data)
        send_notification_request = SendNotificationRequest(Message=message, Type=1, Action=3, AdditionalData=data_list)
        self.dispatcher.dispatch(SendNotificationCommand(request=send_notification_request))
