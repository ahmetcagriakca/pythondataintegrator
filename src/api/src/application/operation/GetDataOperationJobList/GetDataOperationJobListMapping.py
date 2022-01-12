from typing import List

from src.application.operation.GetDataOperationJobList.GetDataOperationJobListDto import GetDataOperationJobListDto
from src.domain.operation import DataOperationJob


class GetDataOperationJobListMapping:
    @staticmethod
    def to_dto(entity: DataOperationJob) -> GetDataOperationJobListDto:
        dto = GetDataOperationJobListDto()
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
    def to_dtos(entities: List[DataOperationJob]) -> List[GetDataOperationJobListDto]:
        result: List[GetDataOperationJobListDto] = []
        for entity in entities:
            dto = GetDataOperationJobListMapping.to_dto(entity=entity)
            result.append(dto)
        return result
