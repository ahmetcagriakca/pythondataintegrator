from typing import List
from domain.common.decorators.responseclass import responseclass
from domain.operation.LookupDataOperation.LookupDataOperationDto import LookupDataOperationDto


@responseclass
class LookupDataOperationResponse:
	Data: List[LookupDataOperationDto] = None
