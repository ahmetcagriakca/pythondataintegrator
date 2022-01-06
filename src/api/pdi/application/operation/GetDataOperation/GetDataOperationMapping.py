from typing import List

from pdip.integrator.connection.domain.enums import ConnectionTypes

from pdi.application.operation.GetDataOperation.GetDataOperationDto import GetDataOperationDto, DataOperationContactDto, \
    DataOperationIntegrationDto, DataIntegrationDto, DataIntegrationColumnDto, ConnectionDto, ConnectionDatabaseDto, \
    ConnectorTypeDto, ConnectionTypeDto, DataIntegrationConnectionDatabaseDto, DataIntegrationConnectionDto
from pdi.domain.operation.DataOperation import DataOperation


class GetDataOperationMapping:
    @staticmethod
    def to_dto(entity: DataOperation) -> GetDataOperationDto:
        dto = GetDataOperationDto()
        dto.Id = entity.Id
        dto.Name = entity.Name
        dto.DefinitionId = entity.DefinitionId
        dto.Version = entity.Definition.Version if entity.Definition is not None else None
        dto.IsDeleted = entity.IsDeleted
        dto.CreationDate = entity.CreationDate
        dto.LastUpdatedDate = entity.LastUpdatedDate
        dto.Contacts = [DataOperationContactDto(Id=contact.Id, Email=contact.Email) for contact in entity.Contacts if
                        contact.IsDeleted == 0]
        data_operation_integrations = []
        for integration in entity.Integrations:
            if integration.IsDeleted == 0:
                data_operation_integration = DataOperationIntegrationDto()
                data_operation_integration.Id = integration.Id
                data_operation_integration.Limit = integration.Limit
                data_operation_integration.ProcessCount = integration.ProcessCount
                data_operation_integration.Order = integration.Order
                data_operation_integration.Integration = DataIntegrationDto()
                data_operation_integration.Integration.Id = integration.DataIntegration.Id
                data_operation_integration.Integration.Code = integration.DataIntegration.Code
                data_operation_integration.Integration.IsTargetTruncate = integration.DataIntegration.IsTargetTruncate
                data_operation_integration.Integration.IsDelta = integration.DataIntegration.IsDelta
                data_operation_integration.Integration.Comments = integration.DataIntegration.Comments

                data_operation_integration.Integration.Columns = [
                    DataIntegrationColumnDto(
                        Id=column.Id,
                        SourceColumnName=column.SourceColumnName,
                        TargetColumnName=column.TargetColumnName
                    ) for column in integration.DataIntegration.Columns if column.IsDeleted == 0]
                for data_integration_connection in integration.DataIntegration.Connections:
                    if data_integration_connection.IsDeleted == 0:
                        connection_type = ConnectionTypeDto(
                            Id=data_integration_connection.Connection.ConnectionType.Id,
                            Name=data_integration_connection.Connection.ConnectionType.Name
                        )
                        connector_type = ConnectorTypeDto(
                            Id=data_integration_connection.Connection.Database.ConnectorType.Id,
                            Name=data_integration_connection.Connection.Database.ConnectorType.Name,
                            ConnectionTypeId=data_integration_connection.Connection.Database.ConnectorType.ConnectionTypeId
                        )
                        connection = ConnectionDto(
                            Id=data_integration_connection.Connection.Id,
                            Name=data_integration_connection.Connection.Name,
                            ConnectionType=connection_type,
                            ConnectionTypeId=data_integration_connection.Connection.ConnectionTypeId,
                            IsDeleted=data_integration_connection.Connection.IsDeleted
                        )
                        database = None
                        if data_integration_connection.Connection.ConnectionTypeId == ConnectionTypes.Sql.value:
                            connection.Database = ConnectionDatabaseDto(
                                Id=data_integration_connection.Connection.Database.Id,
                                Sid=data_integration_connection.Connection.Database.Sid,
                                ServiceName=data_integration_connection.Connection.Database.ServiceName,
                                DatabaseName=data_integration_connection.Connection.Database.DatabaseName,
                                ConnectorType=connector_type
                            )
                            database = DataIntegrationConnectionDatabaseDto(
                                Id=data_integration_connection.Database.Id,
                                Schema=data_integration_connection.Database.Schema,
                                TableName=data_integration_connection.Database.TableName,
                                Query=data_integration_connection.Database.Query)

                        if data_integration_connection.SourceOrTarget == 0:
                            data_operation_integration.Integration.SourceConnection = DataIntegrationConnectionDto(
                                Id=data_integration_connection.Id,
                                Connection=connection,
                                Database=database)
                        elif data_integration_connection.SourceOrTarget == 1:
                            data_operation_integration.Integration.TargetConnection = DataIntegrationConnectionDto(
                                Id=data_integration_connection.Id,
                                Connection=connection,
                                Database=database)

                data_operation_integrations.append(data_operation_integration)
        data_operation_integrations.sort(key=lambda x: getattr(x, 'Order'))
        dto.Integrations = data_operation_integrations
        return dto

    @staticmethod
    def to_dtos(entities: List[DataOperation]) -> List[GetDataOperationDto]:
        result: List[GetDataOperationDto] = []
        for entity in entities:
            dto = GetDataOperationMapping.to_dto(entity=entity)
            result.append(dto)
        return result
