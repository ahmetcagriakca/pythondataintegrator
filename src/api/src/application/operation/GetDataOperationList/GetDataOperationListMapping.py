from typing import List

from src.application.operation.GetDataOperationList.GetDataOperationListDto import GetDataOperationListDto, \
    DataOperationContactDto
from src.domain.operation import DataOperation


class GetDataOperationListMapping:
    @staticmethod
    def to_dto(entity: DataOperation) -> GetDataOperationListDto:
        dto = GetDataOperationListDto()
        dto.Id = entity.Id
        dto.Name = entity.Name
        dto.DefinitionId = entity.DefinitionId
        dto.CreationDate = entity.CreationDate
        dto.LastUpdatedDate = entity.LastUpdatedDate

        dto.Contacts = [DataOperationContactDto(Id=contact.Id, Email=contact.Email) for contact in entity.Contacts if
                        contact.IsDeleted == 0]
        dto.IsDeleted = entity.IsDeleted
        return dto

    @staticmethod
    def to_dtos(entities: List[DataOperation]) -> List[GetDataOperationListDto]:
        result: List[GetDataOperationListDto] = []
        for entity in entities:
            dto = GetDataOperationListMapping.to_dto(entity=entity)
            result.append(dto)
        return result
