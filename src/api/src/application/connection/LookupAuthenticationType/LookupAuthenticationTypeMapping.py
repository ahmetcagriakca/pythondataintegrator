from typing import List

from src.application.connection.LookupAuthenticationType.LookupAuthenticationTypeDto import LookupAuthenticationTypeDto
from src.domain.secret import AuthenticationType


class LookupAuthenticationTypeMapping:
    @staticmethod
    def to_dto(entity: AuthenticationType) -> LookupAuthenticationTypeDto:
        dto = LookupAuthenticationTypeDto()
        dto.Id = entity.Id
        dto.Name = entity.Name
        return dto

    @staticmethod
    def to_dtos(entities: List[AuthenticationType]) -> List[LookupAuthenticationTypeDto]:
        result: List[LookupAuthenticationTypeDto] = []
        for entity in entities:
            dto = LookupAuthenticationTypeMapping.to_dto(entity=entity)
            result.append(dto)
        return result
