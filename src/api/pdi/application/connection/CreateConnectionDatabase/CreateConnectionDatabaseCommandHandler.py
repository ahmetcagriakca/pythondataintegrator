from injector import inject
from pdip.cqrs import Dispatcher
from pdip.cqrs import ICommandHandler
from pdip.data import RepositoryProvider

from pdi.application.connection.CreateConnectionDatabase.CreateConnectionDatabaseCommand import \
    CreateConnectionDatabaseCommand
from pdi.application.connection.services.ConnectionService import ConnectionService
from pdi.application.notification.SendNotification.SendNotificationCommand import SendNotificationCommand
from pdi.application.notification.SendNotification.SendNotificationRequest import SendNotificationRequest, \
    NotificationAdditionalData


class CreateConnectionDatabaseCommandHandler(ICommandHandler[CreateConnectionDatabaseCommand]):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 connection_service: ConnectionService,
                 repository_provider: RepositoryProvider,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repository_provider = repository_provider
        self.dispatcher = dispatcher
        self.connection_service = connection_service

    def handle(self, command: CreateConnectionDatabaseCommand):
        check_existing = self.connection_service.check_connection_name(command.request.Name)
        connection = self.connection_service.create_connection_database(command.request)
        self.repository_provider.commit()
        self.notify(id=connection.Id, name=connection.Name, check_existing=check_existing)

    def notify(self, id: int, name: str, check_existing: bool):
        data_list = []
        data = NotificationAdditionalData(Key="Type", Value="Connection")
        data_list.append(data)
        data = NotificationAdditionalData(Key="Id", Value=id)
        data_list.append(data)
        data = NotificationAdditionalData(Key="Name", Value=name)
        data_list.append(data)
        if check_existing:
            action = 2
            message = f"{name} Connection Updated"
        else:
            action = 1
            message = f"{name} Connection Created"

        send_notification_request = SendNotificationRequest(Message=message, Type=1, Action=action,
                                                            AdditionalData=data_list)
        self.dispatcher.dispatch(SendNotificationCommand(request=send_notification_request))