from typing import List

from sqlalchemy.orm import Query

from domain.operation.GetDataOperationJobExecutionIntegrationList.GetDataOperationJobExecutionIntegrationListDto import \
    GetDataOperationJobExecutionIntegrationListDto
from models.dao.operation.DataOperationJobExecutionIntegration import DataOperationJobExecutionIntegration


class GetDataOperationJobExecutionIntegrationListMapping:
    @staticmethod
    def to_dto(entity: Query) -> GetDataOperationJobExecutionIntegrationListDto:
        dto = GetDataOperationJobExecutionIntegrationListDto()

        dto.Id = entity.DataOperationJobExecutionIntegration.Id
        dto.DataIntegrationId = entity.DataOperationIntegration.DataIntegration.Id
        dto.DataIntegrationCode = entity.DataOperationIntegration.DataIntegration.Code
        dto.Order = entity.DataOperationIntegration.Order
        dto.SourceConnectionName = entity.DataOperationIntegration.Id
        dto.TargetConnectionName = entity.DataOperationIntegration.Id
        dto.Status = entity.DataOperationJobExecutionIntegration.StatusId
        dto.Limit = entity.DataOperationIntegration.Limit
        dto.ProcessCount = entity.DataOperationIntegration.ProcessCount
        dto.SourceDataCount = entity.DataOperationJobExecutionIntegration.SourceDataCount
        dto.AffectedRowCount = entity.AffectedRowCount
        dto.StartDate = entity.DataOperationJobExecutionIntegration.StartDate
        dto.EndDate = entity.DataOperationJobExecutionIntegration.EndDate
        dto.Log = entity.DataOperationJobExecutionIntegration.Log
        dto.CreationDate = entity.DataOperationJobExecutionIntegration.CreationDate
        return dto

    @staticmethod
    def to_dtos(entities: List[DataOperationJobExecutionIntegration]) -> List[
        GetDataOperationJobExecutionIntegrationListDto]:
        result: List[GetDataOperationJobExecutionIntegrationListDto] = []
        for entity in entities:
            dto = GetDataOperationJobExecutionIntegrationListMapping.to_dto(entity=entity)
            result.append(dto)
        return result
