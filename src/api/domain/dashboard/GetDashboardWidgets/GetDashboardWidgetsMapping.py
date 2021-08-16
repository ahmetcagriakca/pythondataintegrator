from typing import List
from domain.dashboard.GetDashboardWidgets.GetDashboardWidgetsDto import GetDashboardWidgetsDto
from models.dao.common.Log import Log


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
