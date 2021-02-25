from typing import List
from injector import inject

from domain.operation.services.DataOperationContactService import DataOperationContactService
from domain.operation.services.DataOperationIntegrationService import DataOperationIntegrationService
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.exception.OperationalException import OperationalException
from infrastructor.logging.SqlLogger import SqlLogger
from models.dao.operation import DataOperation, Definition
from models.dao.operation.DataOperationContact import DataOperationContact
from models.viewmodels.operation import CreateDataOperationModel
from models.viewmodels.operation.UpdateDataOperationModel import UpdateDataOperationModel


class DefinitionService(IScoped):

    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 ):
        self.database_session_manager = database_session_manager
        self.definition_repository: Repository[Definition] = Repository[Definition](database_session_manager)

    def get_all_by_name(self, name: str) -> List[Definition]:
        definitions: List[Definition] = self.definition_repository.filter_by(IsDeleted=0, Name=name)
        return definitions

    def create_definition(self, name, definition_json) -> Definition:
        definitions: List[Definition] = self.get_all_by_name(name=name).order_by(
            "Version").all()
        if definitions is not None and len(definitions) > 0:
            old_definition = definitions[len(definitions) - 1]
            old_definition.IsActive = False
            new_version = old_definition.Version + 1
            definition = Definition(Name=name, Version=new_version, Content=definition_json,
                                    IsActive=True)
        else:
            definition = Definition(Name=name, Version=1, Content=definition_json, IsActive=True)
        self.definition_repository.insert(definition)
        return definition

    def delete_by_name(self, name: int):
        """
        Delete Data operation
        """

        entities = self.get_all_by_name(name=name)
        for entity in entities:
            self.definition_repository.delete_by_id(entity.Id)
