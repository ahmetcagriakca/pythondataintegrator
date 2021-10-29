from typing import List

from pdi.application.connection.GetConnectionList.GetConnectionListDto import GetConnectionListDto, GetConnectorTypeDto, \
    GetConnectionTypeDto
from pdi.domain.connection import Connection


class GetConnectionListMapping:
    @staticmethod
    def to_dto(entity: Connection) -> GetConnectionListDto:
        dto = GetConnectionListDto()
        dto.Id = entity.Id
        dto.Name = entity.Name
        dto.ConnectionType = GetConnectionTypeDto(Id=entity.ConnectionType.Id, Name=entity.ConnectionType.Name)
        dto.ConnectorType = GetConnectorTypeDto(Id=entity.Database.ConnectorType.Id,
                                                Name=entity.Database.ConnectorType.Name)
        dto.Host = entity.ConnectionServers[0].Host
        dto.Port = entity.ConnectionServers[0].Port
        dto.Sid = entity.Database.Sid
        dto.ServiceName = entity.Database.ServiceName
        dto.DatabaseName = entity.Database.DatabaseName
        dto.CreationDate = entity.Database.CreationDate
        dto.IsDeleted = entity.IsDeleted
        return dto

    @staticmethod
    def to_dtos(entities: List[Connection]) -> List[GetConnectionListDto]:
        result: List[GetConnectionListDto] = []
        for entity in entities:
            dto = GetConnectionListMapping.to_dto(entity=entity)
            result.append(dto)
        return result
