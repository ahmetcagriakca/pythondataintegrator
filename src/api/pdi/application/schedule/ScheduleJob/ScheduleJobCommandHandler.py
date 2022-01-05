from injector import inject
from pdip.cqrs import Dispatcher
from pdip.cqrs import ICommandHandler
from pdip.data.repository import RepositoryProvider

from pdi.application.job.services.JobOperationService import JobOperationService
from pdi.application.notification.SendNotification.SendNotificationCommand import SendNotificationCommand
from pdi.application.notification.SendNotification.SendNotificationRequest import NotificationAdditionalData, \
    SendNotificationRequest
from pdi.application.schedule.ScheduleJob.ScheduleJobCommand import ScheduleJobCommand


class ScheduleJobCommandHandler(ICommandHandler[ScheduleJobCommand]):
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

    def handle(self, command: ScheduleJobCommand):
        data_operation_job = self.job_operation_service.insert_job_with_date(
            operation_name=command.request.OperationName,
            run_date=command.request.RunDate)
        self.repository_provider.commit()
        self.notify(id=data_operation_job.Id, name=data_operation_job.DataOperation.Name)

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
