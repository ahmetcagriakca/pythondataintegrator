from typing import List

from domain.connection.GetConnectionList.GetConnectionListDto import GetConnectionListDto
from models.dao.connection import Connection


class GetConnectionListMapping:
    @staticmethod
    def to_dto(entity: Connection) -> GetConnectionListDto:
        dto = GetConnectionListDto()
        dto.Id = entity.Id
        dto.Name = entity.Name
        dto.ConnectorTypeId = entity.Database.ConnectorType.Id
        dto.ConnectorTypeName = entity.Database.ConnectorType.Name
        dto.ConnectionTypeId = entity.ConnectionType.Id
        dto.ConnectionTypeName = entity.ConnectionType.Name
        dto.Host = entity.ConnectionServers[0].Host
        dto.Port = entity.ConnectionServers[0].Port
        dto.Sid = entity.Database.Sid
        dto.ServiceName = entity.Database.ServiceName
        dto.DatabaseName = entity.Database.DatabaseName
        dto.CreationDate = entity.Database.CreationDate
        return dto

    @staticmethod
    def to_dtos(entities: List[Connection]) -> List[GetConnectionListDto]:
        result: List[GetConnectionListDto]=[]
        for entity in entities:
            dto = GetConnectionListMapping.to_dto(entity=entity)
            result.append(dto)
        return result
