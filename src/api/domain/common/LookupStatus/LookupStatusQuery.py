from dataclasses import dataclass
from pdip.cqrs import IQuery
from domain.common.LookupStatus.LookupStatusRequest import LookupStatusRequest
from domain.common.LookupStatus.LookupStatusResponse import LookupStatusResponse


@dataclass
class LookupStatusQuery(IQuery[LookupStatusResponse]):
    request: LookupStatusRequest = None
