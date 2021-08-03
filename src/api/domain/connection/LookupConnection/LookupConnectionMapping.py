from typing import List
from domain.connection.LookupConnection.LookupConnectionDto import LookupConnectionDto
from models.dao.connection.Connection import Connection


class LookupConnectionMapping:
    @staticmethod
    def to_dto(entity: Connection) -> LookupConnectionDto:
        dto = LookupConnectionDto()
        dto.Id=entity.Id
        dto.Name=entity.Name
        dto.ConnectionTypeId=entity.ConnectionTypeId
        return dto

    @staticmethod
    def to_dtos(entities: List[Connection]) -> List[LookupConnectionDto]:
        result: List[LookupConnectionDto] = []
        for entity in entities:
            dto = LookupConnectionMapping.to_dto(entity=entity)
            result.append(dto)
        return result
