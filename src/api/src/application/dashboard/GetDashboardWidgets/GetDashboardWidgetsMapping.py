from typing import List

from src.application.dashboard.GetDashboardWidgets.GetDashboardWidgetsDto import GetDashboardWidgetsDto
from src.domain.common.Log import Log


class GetDashboardWidgetsMapping:
    @staticmethod
    def to_dto(entity: Log) -> GetDashboardWidgetsDto:
        dto = GetDashboardWidgetsDto()
        return dto

    @staticmethod
    def to_dtos(entities: List[Log]) -> List[GetDashboardWidgetsDto]:
        result: List[GetDashboardWidgetsDto] = []
        for entity in entities:
            dto = GetDashboardWidgetsMapping.to_dto(entity=entity)
            result.append(dto)
        return result
