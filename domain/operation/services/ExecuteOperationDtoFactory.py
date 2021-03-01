from typing import List
from injector import inject

from domain.integration.services.DataIntegrationConnectionService import DataIntegrationConnectionService
from domain.integration.services.DataIntegrationService import DataIntegrationService
from infrastructor.dependency.scopes import IScoped
from models.dao.integration.DataIntegrationColumn import DataIntegrationColumn
from models.dao.integration.DataIntegrationConnection import DataIntegrationConnection
from models.dto.ExecuteOperationDto import ExecuteOperationDto


class ExecuteOperationDtoFactory(IScoped):

    @inject
    def __init__(self,
                 data_integration_service: DataIntegrationService,
                 data_integration_connection_service: DataIntegrationConnectionService
                 ):
        self.data_integration_connection_service = data_integration_connection_service
        self.data_integration_service = data_integration_service

    def create_execute_operation_dto(self, data_integration_id: int):
        data_integration = self.data_integration_service.get_by_id(id=data_integration_id)

        source_connection = self.data_integration_connection_service.get_source_connection(
            data_integration_id=data_integration.Id)
        target_connection = self.data_integration_connection_service.get_target_connection(
            data_integration_id=data_integration.Id)

        execute_operation_dto = self.get_execute_operation_dto(
            source_connection=source_connection,
            target_connection=target_connection,
            data_integration_columns=data_integration.Columns)
        return execute_operation_dto

    def get_execute_operation_dto(self,
                                  source_connection: DataIntegrationConnection,
                                  target_connection: DataIntegrationConnection,
                                  data_integration_columns: List[DataIntegrationColumn]):
        column_rows = [(data_integration_column.ResourceType, data_integration_column.SourceColumnName,
                        data_integration_column.TargetColumnName) for data_integration_column in
                       data_integration_columns]
        execute_operation_dto = ExecuteOperationDto(
            source_connection=source_connection,
            target_connection=target_connection,
            source_query=source_connection.Query,
            target_query=target_connection.Query,
            column_rows=column_rows,
            first_row=data_integration_columns[0].SourceColumnName
        )
        return execute_operation_dto
