from dataclasses import dataclass
from pdip.cqrs import IQuery

from pdi.application.common.LookupStatus.LookupStatusRequest import LookupStatusRequest
from pdi.application.common.LookupStatus.LookupStatusResponse import LookupStatusResponse


@dataclass
class LookupStatusQuery(IQuery[LookupStatusResponse]):
    request: LookupStatusRequest = None
