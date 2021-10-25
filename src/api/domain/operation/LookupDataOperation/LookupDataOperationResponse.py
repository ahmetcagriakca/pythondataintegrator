from typing import List
from pdip.cqrs.decorators import responseclass
from domain.operation.LookupDataOperation.LookupDataOperationDto import LookupDataOperationDto


@responseclass
class LookupDataOperationResponse:
	Data: List[LookupDataOperationDto] = None
