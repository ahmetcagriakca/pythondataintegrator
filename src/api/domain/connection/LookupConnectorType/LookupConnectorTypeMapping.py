from typing import List
from domain.connection.LookupConnectorType.LookupConnectorTypeDto import LookupConnectorTypeDto
from models.dao.connection.ConnectorType import ConnectorType


class LookupConnectorTypeMapping:
    @staticmethod
    def to_dto(entity: ConnectorType) -> LookupConnectorTypeDto:
        dto = LookupConnectorTypeDto()
        dto.Id=entity.Id
        dto.Name=entity.Name
        return dto

    @staticmethod
    def to_dtos(entities: List[ConnectorType]) -> List[LookupConnectorTypeDto]:
        result: List[LookupConnectorTypeDto] = []
        for entity in entities:
            dto = LookupConnectorTypeMapping.to_dto(entity=entity)
            result.append(dto)
        return result
