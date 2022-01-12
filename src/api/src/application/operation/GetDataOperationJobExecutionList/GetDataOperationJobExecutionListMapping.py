from typing import List

from sqlalchemy.orm import Query

from src.application.operation.GetDataOperationJobExecutionList.GetDataOperationJobExecutionListDto import \
    GetDataOperationJobExecutionListDto, GetDataOperationScheduleInfoDto
from src.domain.operation.DataOperationJobExecution import DataOperationJobExecution


class GetDataOperationJobExecutionListMapping:
    @staticmethod
    def to_dto(entity: Query) -> GetDataOperationJobExecutionListDto:
        dto = GetDataOperationJobExecutionListDto()
        dto.Id = entity.DataOperationJobExecution.Id
        dto.JobId = entity.DataOperationJob.Id
        dto.DataOperationId = entity.DataOperation.Id
        dto.DataOperationName = entity.DataOperation.Name
        dto.ScheduleInfo = GetDataOperationScheduleInfoDto()
        dto.ScheduleInfo.Cron = entity.DataOperationJob.Cron
        dto.ScheduleInfo.StartDate = entity.DataOperationJob.StartDate
        dto.ScheduleInfo.EndDate = entity.DataOperationJob.EndDate
        dto.StatusId = entity.Status.Id
        dto.StatusDescription = entity.Status.Description
        dto.Log = entity.Log

        dto.SourceDataCount = entity.SourceDataCount
        dto.AffectedRowCount = entity.AffectedRowCount
        dto.StartDate = entity.DataOperationJobExecution.StartDate
        dto.EndDate = entity.DataOperationJobExecution.EndDate
        dto.CreationDate = entity.DataOperationJobExecution.CreationDate
        return dto

    @staticmethod
    def to_dtos(entities: List[DataOperationJobExecution]) -> List[GetDataOperationJobExecutionListDto]:
        result: List[GetDataOperationJobExecutionListDto] = []
        for entity in entities:
            dto = GetDataOperationJobExecutionListMapping.to_dto(entity=entity)
            result.append(dto)
        return result
