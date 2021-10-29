from typing import List

from pdip.cqrs.decorators import responseclass

from pdi.application.common.LookupStatus.LookupStatusDto import LookupStatusDto


@responseclass
class LookupStatusResponse:
    Data: List[LookupStatusDto] = None
