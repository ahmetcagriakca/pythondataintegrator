from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from domain.connection.GetConnectionList.ConnectionListDto import ConnectionListDto
from models.dao.connection import Connection


class ConnectionListMapping:
    @staticmethod
    def to_dto(entity: Connection) -> ConnectionListDto:
        dto = ConnectionListDto()
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
    def to_dtos(entities: List[Connection]) -> List[ConnectionListDto]:
        result: List[ConnectionListDto]=[]
        for entity in entities:
            dto = ConnectionListMapping.to_dto(entity=entity)
            result.append(dto)
        return result
