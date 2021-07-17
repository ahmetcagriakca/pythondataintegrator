from injector import inject
from domain.operation.DeleteDataOperation.DeleteDataOperationCommand import DeleteDataOperationCommand
from domain.operation.services.DataOperationService import DataOperationService
from infrastructure.cqrs.ICommandHandler import ICommandHandler


class DeleteDataOperationCommandHandler(ICommandHandler[DeleteDataOperationCommand]):
    @inject
    def __init__(self,
                 data_operation_service: DataOperationService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_operation_service = data_operation_service

    def handle(self, command: DeleteDataOperationCommand):
        self.data_operation_service.delete_data_operation(command.Id)
