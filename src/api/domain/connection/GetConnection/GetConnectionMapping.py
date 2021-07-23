from typing import List
from domain.connection.GetConnection.GetConnectionDto import GetConnectionDto
from models.dao.connection.Connection import Connection


class GetConnectionMapping:
    @staticmethod
    def to_dto(entity: Connection) -> GetConnectionDto:
        dto = GetConnectionDto()
        dto.Id = entity.Id
        dto.Name = entity.Name
        dto.ConnectorTypeId = entity.Database.ConnectorType.Id
        dto.ConnectionTypeId = entity.ConnectionType.Id
        return dto

    @staticmethod
    def to_dtos(entities: List[Connection]) -> List[GetConnectionDto]:
        result: List[GetConnectionDto] = []
        for entity in entities:
            dto = GetConnectionMapping.to_dto(entity=entity)
            result.append(dto)
        return result
