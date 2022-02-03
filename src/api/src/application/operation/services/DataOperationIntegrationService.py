from typing import List

from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped
from sqlalchemy import or_

from src.application.integration.services.DataIntegrationService import DataIntegrationService
from src.application.operation.CreateDataOperation.CreateDataOperationIntegrationRequest import \
    CreateDataOperationIntegrationRequest
from src.domain.integration import DataIntegration
from src.domain.operation import DataOperation, DataOperationIntegration, Definition


class DataOperationIntegrationService(IScoped):

    @inject
    def __init__(self,
                 data_integration_service: DataIntegrationService,
                 repository_provider: RepositoryProvider,
                 ):
        super().__init__()
        self.repository_provider = repository_provider
        self.data_operation_integration_repository = repository_provider.get(DataOperationIntegration)
        self.data_integration_service = data_integration_service

    def get_all_by_data_operation_id(self, data_operation_id: int) -> List[DataOperationIntegration]:
        entities = self.data_operation_integration_repository.filter_by(
            IsDeleted=0, DataOperationId=data_operation_id)
        return entities

    def get_by_id(self, id: int) -> DataOperationIntegration:
        data_operation_integration = self.data_operation_integration_repository.first(IsDeleted=0, Id=id)
        return data_operation_integration

    def insert(self,
               data_operation: DataOperation,
               data_operation_integration_models: List[CreateDataOperationIntegrationRequest],
               definition: Definition):
        """
        Create Data Operation Integration
        """
        order = 0
        for data_operation_integration_model in data_operation_integration_models:
            order = order + 1
            data_integration = self.data_integration_service.create_data_integration(
                data=data_operation_integration_model.Integration, definition=definition)

            data_operation_integration = DataOperationIntegration(
                Order=order,
                Limit=data_operation_integration_model.Limit,
                ProcessCount=data_operation_integration_model.ProcessCount,
                DataIntegration=data_integration,
                DataOperation=data_operation)
            self.data_operation_integration_repository.insert(data_operation_integration)

    def update(self,
               data_operation: DataOperation,
               data_operation_integration_models: List[CreateDataOperationIntegrationRequest],
               definition: Definition,
               old_definition: Definition,
               ):
        """
        Update Data Operation integration
        """

        order = 0
        for data_operation_integration_model in data_operation_integration_models:
            order = order + 1
            data_integration = self.data_integration_service.check_and_update_data_integration(
                data=data_operation_integration_model.Integration,
                definition=definition,
                old_definition=old_definition)

            data_operation_integration = self.data_operation_integration_repository.first(
                DataOperationId=data_operation.Id,
                DataIntegrationId=data_integration.Id)
            if data_operation_integration is None:
                new_data_operation_integration = DataOperationIntegration(
                    Order=order,
                    Limit=data_operation_integration_model.Limit,
                    ProcessCount=data_operation_integration_model.ProcessCount,
                    DataIntegration=data_integration,
                    DataOperation=data_operation)
                self.data_operation_integration_repository.insert(new_data_operation_integration)
            else:
                data_operation_integration.DataIntegration = data_integration
                data_operation_integration.Order = order
                data_operation_integration.Limit = data_operation_integration_model.Limit
                data_operation_integration.ProcessCount = data_operation_integration_model.ProcessCount
                data_operation_integration.IsDeleted = 0
            un_used_integrations = self.data_operation_integration_repository.table.join(DataIntegration) \
                .filter(DataOperationIntegration.DataOperationId == data_operation.Id) \
                .filter(DataIntegration.Code == data_operation_integration_model.Integration.Code) \
                .filter(DataIntegration.Id != data_integration.Id) \
                .filter(DataIntegration.IsDeleted == 0) \
                .filter(or_(DataIntegration.DefinitionId != definition.Id, DataIntegration.DefinitionId == None)) \
                .filter(DataOperationIntegration.IsDeleted == 0) \
                .all()
            for un_used_integration in un_used_integrations:
                self.delete_by_id(un_used_integration.Id,
                                  definition_id=un_used_integration.DataIntegration.DefinitionId)

        check_existing_integrations = self.get_all_by_data_operation_id(data_operation_id=data_operation.Id).all()
        for existing_integration in check_existing_integrations:
            found = False
            for data_operation_integration_model in data_operation_integration_models:
                if existing_integration.DataIntegration.Code == data_operation_integration_model.Integration.Code and \
                        existing_integration.DataIntegration.IsDeleted == 0:
                    found = True
            if not found:
                self.delete_by_id(existing_integration.Id, old_definition.Id)

    def delete_by_id(self,
                     id: int,
                     definition_id: int):
        data_operation_integration = self.get_by_id(id=id)
        self.data_operation_integration_repository.delete_by_id(id=id)
        if data_operation_integration.DataIntegration.IsDeleted == 0:
            self.data_integration_service.delete_data_integration(code=data_operation_integration.DataIntegration.Code,
                                                                  definition_id=definition_id)

    def delete_by_data_operation_id(self,
                                    data_operation_id: int,
                                    definition_id: int):
        """
        Delete Data operation integration
        """
        check_existing_integrations = self.data_operation_integration_repository.filter_by(
            IsDeleted=0,
            DataOperationId=data_operation_id)
        for existing_integration in check_existing_integrations:
            self.delete_by_id(existing_integration.Id, definition_id=definition_id)
