from typing import List

from src.application.connection.GetConnection.GetConnectionDto import GetConnectionDto, GetConnectionTypeDto
from src.domain.connection.Connection import Connection


class GetConnectionMapping:
    @staticmethod
    def to_dto(entity: Connection) -> GetConnectionDto:
        dto = GetConnectionDto()
        dto.Id = entity.Id
        dto.Name = entity.Name
        dto.ConnectionType = GetConnectionTypeDto(Id=entity.ConnectionType.Id, Name=entity.ConnectionType.Name)
        dto.CreationDate = entity.CreationDate
        dto.IsDeleted = entity.IsDeleted

        return dto

    @staticmethod
    def to_dtos(entities: List[Connection]) -> List[GetConnectionDto]:
        result: List[GetConnectionDto] = []
        for entity in entities:
            dto = GetConnectionMapping.to_dto(entity=entity)
            result.append(dto)
        return result
