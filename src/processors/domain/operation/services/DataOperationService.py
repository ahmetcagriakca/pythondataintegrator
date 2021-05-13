from typing import List
from injector import inject

from domain.operation.services.DataOperationContactService import DataOperationContactService
from domain.operation.services.DataOperationIntegrationService import DataOperationIntegrationService
from domain.operation.services.DefinitionService import DefinitionService
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.exceptions.OperationalException import OperationalException
from infrastructor.logging.SqlLogger import SqlLogger
from models.dao.operation import DataOperation, Definition
from models.viewmodels.operation import DataOperation


class DataOperationService(IScoped):

    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 sql_logger: SqlLogger,
                 data_operation_integration_service: DataOperationIntegrationService,
                 data_operation_contact_service: DataOperationContactService,
                 definition_service: DefinitionService
                 ):
        self.definition_service = definition_service
        self.data_operation_contact_service = data_operation_contact_service
        self.data_operation_integration_service = data_operation_integration_service
        self.sql_logger: SqlLogger = sql_logger
        self.database_session_manager = database_session_manager
        self.data_operation_repository: Repository[DataOperation] = Repository[DataOperation](
            database_session_manager)

    def get_data_operations(self) -> List[DataOperation]:
        """
        Data data_integration data preparing
        """
        data_operations = self.data_operation_repository.filter_by(IsDeleted=0).all()
        return data_operations

    def get_by_id(self, id: int) -> DataOperation:
        data_operation = self.data_operation_repository.first(Id=id, IsDeleted=0)
        return data_operation

    def get_by_name(self, name) -> DataOperation:
        data_operation = self.data_operation_repository.first(Name=name, IsDeleted=0)
        return data_operation

    def get_name(self, id) ->str:
        data_operation = self.get_by_id(id=id)
        return data_operation.Name

    def check_by_name(self, name) -> DataOperation:
        data_operation = self.get_by_name(name=name)
        return data_operation is not None

    def post_data_operation(self, data_operation_model: DataOperation,
                            definition_json: str) -> DataOperation:
        """
        Create Data Operation
        """
        definition: Definition = self.definition_service.create_definition(data_operation_model.Name, definition_json)
        data_operation = self.get_by_name(name=data_operation_model.Name)
        if data_operation is None:
            self.insert_data_operation(data_operation_model, definition)
        else:
            self.update_data_operation(data_operation_model, definition)

        self.database_session_manager.commit()
        data_operation = self.get_by_name(name=data_operation_model.Name)
        return data_operation

    def insert_data_operation(self, data_operation_model: DataOperation,
                              definition: Definition) -> DataOperation:
        """
        Create Data Operation
        """
        if self.check_by_name(data_operation_model.Name):
            raise OperationalException("Name already defined for other data operation")

        data_operation = DataOperation(Name=data_operation_model.Name, Definition=definition)

        self.data_operation_contact_service.insert(data_operation=data_operation,
                                                   data_operation_contact_models=data_operation_model.Contacts)
        self.data_operation_integration_service.insert(data_operation=data_operation,
                                                       data_operation_integration_models=data_operation_model.Integrations,
                                                       definition=definition)

        self.data_operation_repository.insert(data_operation)
        return data_operation

    def update_data_operation(self,
                              data_operation_model: DataOperation,
                              definition: Definition) -> DataOperation:
        """
        Update Data Operation
        """
        if not self.check_by_name(data_operation_model.Name):
            raise OperationalException("Data Operation not found")
        data_operation = self.data_operation_repository.first(IsDeleted=0, Name=data_operation_model.Name)
        # insert or update data_integration
        old_definition = data_operation.Definition
        data_operation.Definition = definition
        self.data_operation_contact_service.update(data_operation=data_operation,
                                                   data_operation_contact_models=data_operation_model.Contacts)

        self.data_operation_integration_service.update(data_operation=data_operation,
                                                       data_operation_integration_models=data_operation_model.Integrations,
                                                       definition=definition,
                                                       old_definition=old_definition)
        return data_operation

    def delete_data_operation(self, id: int):
        """
        Delete Data operation
        """
        data_operation = self.get_by_id(id=id)
        if data_operation is None:
            raise OperationalException("Data Operation Not Found")

        self.data_operation_repository.delete_by_id(data_operation.Id)

        self.data_operation_contact_service.delete_by_data_operation_id(data_operation_id=data_operation.Id)
        self.data_operation_integration_service.delete_by_data_operation_id(data_operation_id=data_operation.Id)
        self.definition_service.delete_by_name(name=data_operation.Name)

        message = f'{data_operation.Name} data operation deleted'
        self.sql_logger.info(message)
        self.database_session_manager.commit()
