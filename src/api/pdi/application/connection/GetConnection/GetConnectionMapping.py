from typing import List

from pdi.application.connection.GetConnection.GetConnectionDto import GetConnectionDto, GetConnectionTypeDto, \
    GetConnectorTypeDto
from pdi.domain.connection.Connection import Connection


class GetConnectionMapping:
    @staticmethod
    def to_dto(entity: Connection) -> GetConnectionDto:
        dto = GetConnectionDto()
        dto.Id = entity.Id
        dto.Name = entity.Name
        dto.ConnectionType = GetConnectionTypeDto(Id=entity.ConnectionType.Id, Name=entity.ConnectionType.Name)
        dto.ConnectorType = GetConnectorTypeDto(Id=entity.Database.ConnectorType.Id,
                                                Name=entity.Database.ConnectorType.Name,
                                                ConnectionTypeId=entity.Database.ConnectorType.ConnectionTypeId)
        dto.Host = entity.ConnectionServers[0].Host
        dto.Port = entity.ConnectionServers[0].Port
        dto.Sid = entity.Database.Sid
        dto.ServiceName = entity.Database.ServiceName
        dto.DatabaseName = entity.Database.DatabaseName
        dto.CreationDate = entity.Database.CreationDate
        dto.IsDeleted = entity.IsDeleted
        return dto

    @staticmethod
    def to_dtos(entities: List[Connection]) -> List[GetConnectionDto]:
        result: List[GetConnectionDto] = []
        for entity in entities:
            dto = GetConnectionMapping.to_dto(entity=entity)
            result.append(dto)
        return result
