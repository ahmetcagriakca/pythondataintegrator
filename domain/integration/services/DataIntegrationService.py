from typing import List

from injector import inject

from domain.integration.services.DataIntegrationColumnService import DataIntegrationColumnService
from domain.integration.services.DataIntegrationConnectionService import DataIntegrationConnectionService
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.exception.OperationalException import OperationalException
from infrastructor.logging.SqlLogger import SqlLogger
from models.dao.operation import Definition
from models.viewmodels.integration.CreateDataIntegrationModel import CreateDataIntegrationModel
from models.dao.integration.DataIntegration import DataIntegration
from models.viewmodels.integration.UpdateDataIntegrationModel import UpdateDataIntegrationModel


class DataIntegrationService(IScoped):
    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 data_integration_column_service: DataIntegrationColumnService,
                 data_integration_connection_service: DataIntegrationConnectionService,

                 ):
        self.data_integration_connection_service = data_integration_connection_service
        self.data_integration_column_service = data_integration_column_service
        self.database_session_manager = database_session_manager
        self.data_integration_repository: Repository[DataIntegration] = Repository[DataIntegration](
            database_session_manager)

    #######################################################################################

    def get_by_id(self, id: int) -> DataIntegration:
        """
        Data data_integration data preparing
        """
        entity = self.data_integration_repository.first(IsDeleted=0, Id=id)
        return entity

    def get_data_integrations(self) -> List[DataIntegration]:
        """
        Data data_integration data preparing
        """
        entites = self.data_integration_repository.filter_by(IsDeleted=0)
        return entites.all()

    def get_is_target_truncate(self, id:int) -> bool:
        entity = self.get_by_id(id=id)
        return entity.IsTargetTruncate

    def check_and_update_data_integration(self,
                                          data: CreateDataIntegrationModel,
                                          definition: Definition,
                                          old_definition: Definition
                                          ) -> DataIntegration:

        if data.IsTargetTruncate \
                and ((data.TargetSchema is None or data.TargetSchema == '') \
                     or (data.TargetTableName is None or data.TargetTableName == '')):
            raise OperationalException("TargetSchema and TargetTableName cannot be empty if IsTargetTruncate is true")
        if old_definition is not None:
            data_integration = self.data_integration_repository.first(IsDeleted=0,
                                                                      Code=data.Code,
                                                                      DefinitionId=old_definition.Id)
        else:
            data_integration = self.data_integration_repository.first(IsDeleted=0,
                                                                      Code=data.Code)
        if data_integration is None:
            data_integration = self.insert_data_integration(data=data, definition=definition)
        else:
            data_integration = self.update_data_integration(data_integration=data_integration, data=data,
                                                            definition=definition)
        return data_integration

    def create_data_integration(self,
                                data: CreateDataIntegrationModel,
                                definition: Definition):

        if data.IsTargetTruncate \
                and ((data.TargetSchema is None or data.TargetSchema == '') \
                     or (data.TargetTableName is None or data.TargetTableName == '')):
            raise OperationalException("TargetSchema and TargetTableName cannot be empty if IsTargetTruncate is true")

        if data.Code is not None and data.Code != "":
            data_integration = self.data_integration_repository.first(IsDeleted=0, Code=data.Code,
                                                                      DefinitionId=definition.Id)
            if data_integration is not None:
                raise OperationalException(f"{data_integration.Code} code already exists")
        else:
            raise OperationalException("Code required")
        data_integration = self.insert_data_integration(data, definition)
        data_integration_result = self.data_integration_repository.first(IsDeleted=0, Id=data_integration.Id)
        return data_integration_result

    def insert_data_integration(self,
                                data: CreateDataIntegrationModel,
                                definition: Definition) -> DataIntegration:

        data_integration = DataIntegration(Code=data.Code, IsTargetTruncate=data.IsTargetTruncate,
                                           IsDelta=data.IsDelta, Definition=definition)
        self.data_integration_repository.insert(data_integration)
        self.data_integration_column_service.insert(
            data_integration=data_integration,
            source_columns=data.SourceColumns,
            target_columns=data.TargetColumns)

        self.data_integration_connection_service.insert(data_integration=data_integration, data=data)

        return data_integration

    def update_data_integration(self,
                                data_integration: DataIntegration,
                                data: UpdateDataIntegrationModel,
                                definition: Definition) -> DataIntegration:
        data_integration.IsTargetTruncate = data.IsTargetTruncate
        data_integration.IsDelta = data.IsDelta
        data_integration.Definition = definition

        self.data_integration_column_service.update(
            data_integration=data_integration,
            source_columns=data.SourceColumns,
            target_columns=data.TargetColumns)

        self.data_integration_connection_service.update(data_integration=data_integration, data=data)

        return data_integration

    def delete_data_integration(self, code):

        if code is not None and code != "":
            data_integration = self.data_integration_repository.first(IsDeleted=0, Code=code)
            if data_integration is None:
                raise OperationalException("Code not found")
        else:
            return "Code required"
        self.data_integration_repository.delete_by_id(id=data_integration.Id)
        for data_integration_connection in data_integration.Connections:
            self.data_integration_connection_service.delete(data_integration_connection.Id)
        for data_integration_column in data_integration.Columns:
            self.data_integration_column_service.delete(data_integration_column.Id)
