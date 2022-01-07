from typing import List

from pdip.integrator.connection.domain.enums import ConnectionTypes

from src.application.connection.GetConnectionList.GetConnectionListDto import GetConnectionListDto, GetConnectorTypeDto, \
    GetConnectionTypeDto
from src.domain.connection import Connection


class GetConnectionListMapping:
    @staticmethod
    def to_dto(entity: Connection) -> GetConnectionListDto:
        dto = GetConnectionListDto()
        dto.Id = entity.Id
        dto.Name = entity.Name
        dto.ConnectionType = GetConnectionTypeDto(Id=entity.ConnectionType.Id, Name=entity.ConnectionType.Name)
        dto.Host = entity.ConnectionServers[0].Host
        dto.Port = entity.ConnectionServers[0].Port
        dto.CreationDate = entity.CreationDate
        dto.IsDeleted = entity.IsDeleted
        if ConnectionTypes(entity.ConnectionType.Id) == ConnectionTypes.Sql:
            dto.ConnectorType = GetConnectorTypeDto(
                Id=entity.Database.ConnectorType.Id,
                Name=entity.Database.ConnectorType.Name
            )
            dto.Sid = entity.Database.Sid
            dto.ServiceName = entity.Database.ServiceName
            dto.DatabaseName = entity.Database.DatabaseName
        elif ConnectionTypes(entity.ConnectionType.Id) == ConnectionTypes.BigData:
            dto.ConnectorType = GetConnectorTypeDto(
                Id=entity.BigData.ConnectorType.Id,
                Name=entity.BigData.ConnectorType.Name
            )
            dto.DatabaseName = entity.BigData.DatabaseName

        return dto

    @staticmethod
    def to_dtos(entities: List[Connection]) -> List[GetConnectionListDto]:
        result: List[GetConnectionListDto] = []
        for entity in entities:
            dto = GetConnectionListMapping.to_dto(entity=entity)
            result.append(dto)
        return result
