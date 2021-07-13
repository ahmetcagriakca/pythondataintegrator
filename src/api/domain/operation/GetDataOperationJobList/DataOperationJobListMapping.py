from typing import List

from domain.operation.GetDataOperationJobList.DataOperationJobListDto import DataOperationJobListDto
from models.dao.operation import DataOperationJob


class DataOperationJobListMapping:
    @staticmethod
    def to_dto(entity: DataOperationJob) -> DataOperationJobListDto:
        dto = DataOperationJobListDto()
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
    def to_dtos(entities: List[DataOperationJob]) -> List[DataOperationJobListDto]:
        result: List[DataOperationJobListDto] = []
        for entity in entities:
            dto = DataOperationJobListMapping.to_dto(entity=entity)
            result.append(dto)
        return result
