from typing import List

from pdi.application.connection.LookupConnectorType.LookupConnectorTypeDto import LookupConnectorTypeDto
from pdi.domain.connection.ConnectorType import ConnectorType


class LookupConnectorTypeMapping:
    @staticmethod
    def to_dto(entity: ConnectorType) -> LookupConnectorTypeDto:
        dto = LookupConnectorTypeDto()
        dto.Id = entity.Id
        dto.Name = entity.Name
        dto.ConnectionTypeId = entity.ConnectionTypeId
        return dto

    @staticmethod
    def to_dtos(entities: List[ConnectorType]) -> List[LookupConnectorTypeDto]:
        result: List[LookupConnectorTypeDto] = []
        for entity in entities:
            dto = LookupConnectorTypeMapping.to_dto(entity=entity)
            result.append(dto)
        return result
