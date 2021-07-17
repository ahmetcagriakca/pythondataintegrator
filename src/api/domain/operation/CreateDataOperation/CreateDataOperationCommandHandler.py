from injector import inject
from domain.operation.CreateDataOperation.CreateDataOperationCommand import CreateDataOperationCommand
from domain.operation.services.DataOperationService import DataOperationService
from infrastructure.cqrs.ICommandHandler import ICommandHandler


class CreateDataOperationCommandHandler(ICommandHandler[CreateDataOperationCommand]):
    @inject
    def __init__(self,
                 data_operation_service: DataOperationService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_operation_service = data_operation_service

    def handle(self, command: CreateDataOperationCommand):
        self.data_operation_service.create(command)
        # data: CreateDataOperationModel = JsonConvert.FromJSON(json.dumps(IocManager.api.payload))
        # creation_result = self.data_operation_service.post_data_operation(
        #     data_operation_model=data,
        #     definition_json=JsonConvert.ToJSON(data))
        # result = DataOperationModels.get_data_operation_result_model(creation_result)
        # return CommonModels.get_response(result=result)
