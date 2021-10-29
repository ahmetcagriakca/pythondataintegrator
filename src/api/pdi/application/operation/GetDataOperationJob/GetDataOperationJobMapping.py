from typing import List

from pdi.application.operation.GetDataOperationJob.GetDataOperationJobDto import GetDataOperationJobDto
from pdi.domain.operation.DataOperationJob import DataOperationJob


class GetDataOperationJobMapping:
    @staticmethod
    def to_dto(entity: DataOperationJob) -> GetDataOperationJobDto:
        dto = GetDataOperationJobDto()
        dto.Id = entity.Id
        dto.JobId = entity.ApSchedulerJobId
        dto.DataOperationId = entity.DataOperation.Id
        dto.DataOperationName = entity.DataOperation.Name
        dto.Cron = entity.Cron
        dto.StartDate = entity.StartDate
        dto.EndDate = entity.EndDate
        dto.NextRunTime = entity.ApSchedulerJob.NextRunTime
        dto.CreationDate = entity.CreationDate
        dto.LastUpdatedDate = entity.LastUpdatedDate
        dto.IsDeleted = entity.IsDeleted
        return dto

    @staticmethod
    def to_dtos(entities: List[DataOperationJob]) -> List[GetDataOperationJobDto]:
        result: List[GetDataOperationJobDto] = []
        for entity in entities:
            dto = GetDataOperationJobMapping.to_dto(entity=entity)
            result.append(dto)
        return result
