from typing import List
from pdip.cqrs.decorators import responseclass
from domain.common.LookupStatus.LookupStatusDto import LookupStatusDto


@responseclass
class LookupStatusResponse:
	Data: List[LookupStatusDto] = None
