from typing import List

from src.application.connection.LookupConnectionType.LookupConnectionTypeDto import LookupConnectionTypeDto
from src.domain.connection.ConnectionType import ConnectionType


class LookupConnectionTypeMapping:
    @staticmethod
    def to_dto(entity: ConnectionType) -> LookupConnectionTypeDto:
        dto = LookupConnectionTypeDto()
        dto.Id = entity.Id
        dto.Name = entity.Name
        return dto

    @staticmethod
    def to_dtos(entities: List[ConnectionType]) -> List[LookupConnectionTypeDto]:
        result: List[LookupConnectionTypeDto] = []
        for entity in entities:
            dto = LookupConnectionTypeMapping.to_dto(entity=entity)
            result.append(dto)
        return result
