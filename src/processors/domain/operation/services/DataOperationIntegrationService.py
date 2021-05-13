from typing import List
from injector import inject

from domain.integration.services.DataIntegrationService import DataIntegrationService
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from models.dao.operation import DataOperation, DataOperationIntegration, Definition
from models.viewmodels.operation.DataOperationIntegration import DataOperationIntegration


class DataOperationIntegrationService(IScoped):

    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 data_integration_service: DataIntegrationService,
                 ):
        self.data_integration_service = data_integration_service
        self.database_session_manager = database_session_manager
        self.data_operation_integration_repository: Repository[DataOperationIntegration] = Repository[
            DataOperationIntegration](database_session_manager)

    def get_all_by_data_operation_id(self, data_operation_id: int) -> List[DataOperationIntegration]:
        entitites = self.data_operation_integration_repository.filter_by(
            IsDeleted=0, DataOperationId=data_operation_id)
        return entitites

    def get_by_id(self, id: int) -> DataOperationIntegration:
        data_operation_integration = self.data_operation_integration_repository.first(IsDeleted=0, Id=id)
        return data_operation_integration

    def insert(self,
               data_operation: DataOperation,
               data_operation_integration_models: List[DataOperationIntegration],
               definition: Definition):
        """
        Create Data Operation Integration
        """
        order = 0
        for data_operation_integration_model in data_operation_integration_models:
            order = order + 1
            data_integration = self.data_integration_service.create_data_integration(
                data=data_operation_integration_model.Integration, definition=definition)

            data_operation_integration = DataOperationIntegration(Order=order,
                                                                  Limit=data_operation_integration_model.Limit,
                                                                  ProcessCount=data_operation_integration_model.ProcessCount,
                                                                  DataIntegration=data_integration,
                                                                  DataOperation=data_operation)
            self.data_operation_integration_repository.insert(data_operation_integration)

    def update(self,
               data_operation: DataOperation,
               data_operation_integration_models: List[DataOperationIntegration],
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
                new_data_operation_integration = DataOperationIntegration(Order=order,
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

        check_existing_integrations = self.get_all_by_data_operation_id(data_operation_id=data_operation.Id).all()
        for existing_integration in check_existing_integrations:
            founded = False
            for data_operation_integration_model in data_operation_integration_models:
                if existing_integration.DataIntegration.Code == data_operation_integration_model.Integration.Code and existing_integration.DataIntegration.IsDeleted == 0:
                    founded = True
            if not founded:
                self.delete_by_id(existing_integration.Id)

    def delete_by_id(self, id: int):
        data_operation_integration = self.get_by_id(id=id)
        self.data_operation_integration_repository.delete_by_id(id=id)
        self.data_integration_service.delete_data_integration(data_operation_integration.DataIntegration.Code)

    def delete_by_data_operation_id(self, data_operation_id: int):
        """
        Delete Data operation integration
        """
        check_existing_integrations = self.data_operation_integration_repository.filter_by(IsDeleted=0,
                                                                                           DataOperationId=data_operation_id)
        for existing_integration in check_existing_integrations:
            self.delete_by_id(existing_integration.Id)
