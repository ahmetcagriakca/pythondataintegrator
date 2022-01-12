from typing import List

from src.application.operation.GetDataOperationJobExecutionLogList.GetDataOperationJobExecutionLogListDto import \
    GetDataOperationJobExecutionLogListDto
from src.domain.common.Log import Log


class GetDataOperationJobExecutionLogListMapping:
    @staticmethod
    def to_dto(entity: Log) -> GetDataOperationJobExecutionLogListDto:
        dto = GetDataOperationJobExecutionLogListDto()
        dto.Id = entity.Id
        dto.CreationDate = entity.CreationDate
        dto.Comments = entity.Comments
        dto.Content = entity.Content.replace('\r\n', '\n')
        return dto

    @staticmethod
    def to_dtos(entities: List[Log]) -> List[GetDataOperationJobExecutionLogListDto]:
        result: List[GetDataOperationJobExecutionLogListDto] = []
        for entity in entities:
            dto = GetDataOperationJobExecutionLogListMapping.to_dto(entity=entity)
            result.append(dto)
        return result
