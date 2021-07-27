import json
from injector import inject
from infrastructure.dependency.scopes import IScoped
from infrastructure.json.DateTimeEncoder import DateTimeEncoder
from domain.operation.CreateDataOperation.CreateDataOperationCommand import CreateDataOperationCommand
from domain.operation.services.DataOperationService import DataOperationService
from infrastructure.cqrs.ICommandHandler import ICommandHandler


class CreateDataOperationCommandHandler(ICommandHandler[CreateDataOperationCommand], IScoped):
    @inject
    def __init__(self,
                 data_operation_service: DataOperationService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_operation_service = data_operation_service

    def handle(self, command: CreateDataOperationCommand):
        definition_json = json.dumps(command.request.to_dict(), cls=DateTimeEncoder, indent=4)
        self.data_operation_service.post_data_operation(
            data_operation_model=command.request,
            definition_json=definition_json)
