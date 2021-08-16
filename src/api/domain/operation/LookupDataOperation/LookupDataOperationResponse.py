from typing import List
from infrastructure.cqrs.decorators.responseclass import responseclass
from domain.operation.LookupDataOperation.LookupDataOperationDto import LookupDataOperationDto


@responseclass
class LookupDataOperationResponse:
	Data: List[LookupDataOperationDto] = None
