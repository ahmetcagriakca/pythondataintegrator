import os
from time import time
from typing import List
from injector import inject

from domain.integration.services.DataIntegrationConnectionService import DataIntegrationConnectionService
from domain.integration.services.DataIntegrationService import DataIntegrationService
from domain.operation.services.DataOperationIntegrationService import DataOperationIntegrationService
from domain.operation.services.DataOperationJobExecutionService import DataOperationJobExecutionService
from domain.operation.services.DataOperationService import DataOperationService
from domain.process.services.ProcessService import ProcessService
from infrastructor.IocManager import IocManager
from infrastructor.data.ConnectionManager import ConnectionManager
from infrastructor.data.ConnectionProvider import ConnectionProvider
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
from infrastructor.multi_processing.ParallelMultiProcessing import TaskData
from models.dao.integration.DataIntegration import DataIntegration
from models.dao.integration.DataIntegrationColumn import DataIntegrationColumn
from models.dao.integration.DataIntegrationConnection import DataIntegrationConnection
from models.dao.integration.DataIntegrationExecutionJob import DataIntegrationExecutionJob
from models.dao.operation import DataOperationIntegration, DataOperationJob
from models.dto.ExecuteOperationDto import ExecuteOperationDto
from models.dto.LimitModifier import LimitModifier
from models.enums.events import EVENT_EXECUTION_STARTED, EVENT_EXECUTION_FINISHED, \
    EVENT_EXECUTION_INTEGRATION_EXECUTE_TRUNCATE, EVENT_EXECUTION_INTEGRATION_EXECUTE_QUERY, \
    EVENT_EXECUTION_INTEGRATION_FINISHED, EVENT_EXECUTION_INTEGRATION_EXECUTE_OPERATION


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
