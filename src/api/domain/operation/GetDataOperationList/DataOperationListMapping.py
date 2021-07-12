from typing import List

from domain.operation.GetDataOperationList.DataOperationListDto import DataOperationListDto, DataOperationContactDto
from models.dao.operation import DataOperation


class DataOperationListMapping:
    @staticmethod
    def to_dto(entity: DataOperation) -> DataOperationListDto:
        dto = DataOperationListDto()
        dto.Id = entity.Id
        dto.Name = entity.Name
        dto.DefinitionId = entity.DefinitionId
        dto.CreationDate = entity.CreationDate
        dto.LastUpdatedDate = entity.LastUpdatedDate

        dto.Contacts = [DataOperationContactDto(Id=contact.Id, Email=contact.Email) for contact in entity.Contacts if
                        contact.IsDeleted == 0]
        return dto

    @staticmethod
    def to_dtos(entities: List[DataOperation]) -> List[DataOperationListDto]:
        result: List[DataOperationListDto] = []
        for entity in entities:
            dto = DataOperationListMapping.to_dto(entity=entity)
            result.append(dto)
        return result
