from typing import List

from pdip.cqrs.decorators import responseclass

from src.application.operation.LookupDataOperation.LookupDataOperationDto import LookupDataOperationDto


@responseclass
class LookupDataOperationResponse:
    Data: List[LookupDataOperationDto] = None
