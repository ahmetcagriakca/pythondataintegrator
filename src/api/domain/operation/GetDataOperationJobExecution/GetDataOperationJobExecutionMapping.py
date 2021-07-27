from typing import List
from domain.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionDto import \
    GetDataOperationJobExecutionDto, GetDataOperationScheduleInfoDto
from models.dao.operation.DataOperationJobExecution import DataOperationJobExecution


class GetDataOperationJobExecutionMapping:
    @staticmethod
    def to_dto(entity: DataOperationJobExecution) -> GetDataOperationJobExecutionDto:
        dto = GetDataOperationJobExecutionDto()
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
    def to_dtos(entities: List[DataOperationJobExecution]) -> List[GetDataOperationJobExecutionDto]:
        result: List[GetDataOperationJobExecutionDto] = []
        for entity in entities:
            dto = GetDataOperationJobExecutionMapping.to_dto(entity=entity)
            result.append(dto)
        return result
