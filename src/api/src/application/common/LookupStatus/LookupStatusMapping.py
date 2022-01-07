from typing import List

from src.application.common.LookupStatus.LookupStatusDto import LookupStatusDto
from src.domain.common.Status import Status


class LookupStatusMapping:
    @staticmethod
    def to_dto(entity: Status) -> LookupStatusDto:
        dto = LookupStatusDto()
        dto.Id = entity.Id
        dto.Name = entity.Name
        return dto

    @staticmethod
    def to_dtos(entities: List[Status]) -> List[LookupStatusDto]:
        result: List[LookupStatusDto] = []
        for entity in entities:
            dto = LookupStatusMapping.to_dto(entity=entity)
            result.append(dto)
        return result
