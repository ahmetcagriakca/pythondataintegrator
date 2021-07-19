from injector import inject

from infrastructure.dependency.scopes import IScoped
from infrastructure.json.JsonConvert import JsonConvert
from domain.operation.CreateDataOperation.CreateDataOperationCommand import CreateDataOperationCommand
from domain.operation.services.DataOperationService import DataOperationService
from infrastructure.cqrs.ICommandHandler import ICommandHandler


class CreateDataOperationCommandHandler(ICommandHandler[CreateDataOperationCommand],IScoped):
    @inject
    def __init__(self,
                 data_operation_service: DataOperationService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_operation_service = data_operation_service

    def handle(self, command: CreateDataOperationCommand):
        self.data_operation_service.post_data_operation(
            data_operation_model=command.request,
            definition_json=JsonConvert.ToJSON(command.request))
