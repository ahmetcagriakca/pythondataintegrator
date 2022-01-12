from dataclasses import dataclass
from pdip.cqrs import IQuery

from src.application.common.LookupStatus.LookupStatusRequest import LookupStatusRequest
from src.application.common.LookupStatus.LookupStatusResponse import LookupStatusResponse


@dataclass
class LookupStatusQuery(IQuery[LookupStatusResponse]):
    request: LookupStatusRequest = None
