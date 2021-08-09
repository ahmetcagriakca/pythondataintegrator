from typing import List
from infrastructure.cqrs.decorators.responseclass import responseclass
from domain.common.LookupStatus.LookupStatusDto import LookupStatusDto


@responseclass
class LookupStatusResponse:
	Data: List[LookupStatusDto] = None
