from typing import List

from pdi.application.connection.GetConnectionSql.GetConnectionSqlDto import GetConnectionSqlDto, GetConnectionTypeDto, \
    GetConnectorTypeDto
from pdi.domain.connection.Connection import Connection


class GetConnectionSqlMapping:
    @staticmethod
    def to_dto(entity: Connection) -> GetConnectionSqlDto:
        dto = GetConnectionSqlDto()
        dto.Id = entity.Id
        dto.Name = entity.Name
        dto.ConnectionType = GetConnectionTypeDto(Id=entity.ConnectionType.Id, Name=entity.ConnectionType.Name)
        dto.Host = entity.ConnectionServers[0].Host
        dto.Port = entity.ConnectionServers[0].Port
        dto.CreationDate = entity.CreationDate
        dto.IsDeleted = entity.IsDeleted

        dto.ConnectorType = GetConnectorTypeDto(Id=entity.Database.ConnectorType.Id,
                                                Name=entity.Database.ConnectorType.Name,
                                                ConnectionTypeId=entity.Database.ConnectorType.ConnectionTypeId)
        dto.Sid = entity.Database.Sid
        dto.ServiceName = entity.Database.ServiceName
        dto.DatabaseName = entity.Database.DatabaseName
        return dto

    @staticmethod
    def to_dtos(entities: List[Connection]) -> List[GetConnectionSqlDto]:
        result: List[GetConnectionSqlDto] = []
        for entity in entities:
            dto = GetConnectionSqlMapping.to_dto(entity=entity)
            result.append(dto)
        return result
