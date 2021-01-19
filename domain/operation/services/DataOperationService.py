from typing import List
from injector import inject

from domain.integration.services.DataIntegrationService import DataIntegrationService
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.exception.OperationalException import OperationalException
from infrastructor.logging.SqlLogger import SqlLogger
from models.dao.integration.DataIntegration import DataIntegration
from models.dao.operation import DataOperation, DataOperationIntegration
from models.dao.operation.DataOperationContact import DataOperationContact
from models.viewmodels.operation import CreateDataOperationModel
from models.viewmodels.operation.UpdateDataOperationModel import UpdateDataOperationModel


class DataOperationService(IScoped):

    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 sql_logger: SqlLogger,
                 data_integration_service: DataIntegrationService,
                 ):
        self.data_integration_service = data_integration_service
        self.database_session_manager = database_session_manager
        self.data_integration_repository: Repository[DataIntegration] = Repository[
            DataIntegration](
            database_session_manager)
        self.data_operation_repository: Repository[DataOperation] = Repository[DataOperation](
            database_session_manager)

        self.data_operation_contact_repository: Repository[DataOperationContact] = Repository[
            DataOperationContact](database_session_manager)
        self.data_operation_integration_repository: Repository[DataOperationIntegration] = Repository[
            DataOperationIntegration](database_session_manager)
        self.sql_logger: SqlLogger = sql_logger

    def get_data_operations(self) -> List[DataOperation]:
        """
        Data data_integration data preparing
        """
        data_operations = self.data_operation_repository.filter_by(IsDeleted=0).all()
        return data_operations

    def check_data_operation_name(self, name) -> DataOperation:
        data_operation = self.data_operation_repository.first(Name=name, IsDeleted=0)
        return data_operation is not None

    def post_data_operation(self, data_operation_model: CreateDataOperationModel) -> DataOperation:
        """
        Create Data Operation
        """
        data_operation = self.data_operation_repository.first(Name=data_operation_model.Name, IsDeleted=0)
        if data_operation is None:
            return self.insert_data_operation(data_operation_model)
        else:
            return self.update_data_operation(data_operation_model)

    def insert_data_operation(self, data_operation_model: CreateDataOperationModel) -> DataOperation:
        """
        Create Data Operation
        """
        if self.check_data_operation_name(data_operation_model.Name):
            raise OperationalException("Name already defined for other data operation")
        data_operation = DataOperation(Name=data_operation_model.Name)

        self.data_operation_repository.insert(data_operation)
        if data_operation_model.Contacts is not None and len(data_operation_model.Contacts)>0:
            for operation_contact in data_operation_model.Contacts:
                data_operation_contact = DataOperationContact(Email=operation_contact.Email,
                                                              DataOperation=data_operation)
                self.data_operation_contact_repository.insert(data_operation_contact)
        order = 0
        for operation_integration in data_operation_model.Integrations:
            order = order + 1
            data_integration = self.data_integration_service.create_data_integration(
                data=operation_integration.Integration)

            data_operation_integration = DataOperationIntegration(Order=order, Limit=operation_integration.Limit,
                                                                  ProcessCount=operation_integration.ProcessCount,
                                                                  DataIntegration=data_integration,
                                                                  DataOperation=data_operation)
            self.data_operation_integration_repository.insert(data_operation_integration)

        self.database_session_manager.commit()

        data_operation = self.data_operation_repository.first(Id=data_operation.Id)
        return data_operation

    def update_data_operation(self,
                              data_operation_model: UpdateDataOperationModel) -> DataOperation:
        """
        Update Data Operation
        """
        if not self.check_data_operation_name(data_operation_model.Name):
            raise OperationalException("Data Operation not found")
        data_operation = self.data_operation_repository.first(Name=data_operation_model.Name)
        # insert or update data_integration

        if data_operation_model.Contacts is not None and len(data_operation_model.Contacts)>0:
            for operation_contact in data_operation_model.Contacts:
                data_operation_contact = self.data_operation_contact_repository.first(IsDeleted=0,
                                                                                      DataOperationId=data_operation.Id,
                                                                                      Email=operation_contact.Email)
                if data_operation_contact is None:
                    data_operation_contact = DataOperationContact(Email=operation_contact.Email,
                                                                  DataOperation=data_operation)
                    self.data_operation_contact_repository.insert(data_operation_contact)

        check_existing_contacts = self.data_operation_contact_repository.filter_by(IsDeleted=0,
                                                                                   DataOperationId=data_operation.Id).all()
        for existing_contact in check_existing_contacts:
            founded = False

            if data_operation_model.Contacts is not None and len(data_operation_model.Contacts) > 0:
                for operation_contact in data_operation_model.Contacts:
                    if existing_contact.Email == operation_contact.Email:
                        founded = True

            if not founded:
                self.data_operation_contact_repository.delete_by_id(existing_contact.Id)

        order = 0
        for operation_integration in data_operation_model.Integrations:
            order = order + 1
            data_integration = self.data_integration_repository.first(IsDeleted=0,
                                                                      Code=operation_integration.Integration.Code)
            if data_integration is None:
                data_integration = self.data_integration_service.create_data_integration(
                    data=operation_integration.Integration)
            else:
                self.data_integration_service.update_data_integration(data=operation_integration.Integration)

            data_operation_integration = self.data_operation_integration_repository.first(
                DataOperationId=data_operation.Id,
                DataIntegrationId=data_integration.Id)
            if data_operation_integration is None:
                new_data_operation_integration = DataOperationIntegration(Order=order,
                                                                          Limit=operation_integration.Limit,
                                                                          ProcessCount=operation_integration.ProcessCount,
                                                                          DataIntegration=data_integration,
                                                                          DataOperation=data_operation)
                self.data_operation_integration_repository.insert(new_data_operation_integration)
            else:
                data_operation_integration.Order = order
                data_operation_integration.Limit = operation_integration.Limit
                data_operation_integration.ProcessCount = operation_integration.ProcessCount
                data_operation_integration.IsDeleted = 0

        check_existing_integrations = self.data_operation_integration_repository.filter_by(IsDeleted=0,
                                                                                           DataOperationId=data_operation.Id)
        for existing_integration in check_existing_integrations:
            founded = False
            for operation_integration in data_operation_model.Integrations:
                if existing_integration.DataIntegration.Code == operation_integration.Integration.Code:
                    founded = True
            if not founded:
                self.data_operation_integration_repository.delete_by_id(existing_integration.Id)
                self.data_integration_service.delete_data_integration(data_operation_integration.DataIntegration.Code)
        self.database_session_manager.commit()

        data_operation = self.data_operation_repository.first(Id=data_operation.Id)

        return data_operation

    def delete_data_operation(self, id: int):
        """
        Delete Data operation
        """
        data_operation = self.data_operation_repository.first(Id=id, IsDeleted=0)
        if data_operation is None:
            raise OperationalException("Data Operation Not Found")

        self.data_operation_repository.delete_by_id(data_operation.Id)
        check_existing_integrations = self.data_operation_integration_repository.filter_by(IsDeleted=0,
                                                                                           DataOperationId=data_operation.Id)
        for existing_integration in check_existing_integrations:
            self.data_operation_integration_repository.delete_by_id(existing_integration.Id)
            self.data_integration_service.delete_data_integration(existing_integration.DataIntegration.Code)
        message = f'{data_operation.Name} data operation deleted'
        self.sql_logger.info(message)
        self.database_session_manager.commit()
