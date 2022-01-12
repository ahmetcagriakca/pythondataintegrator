from dataclasses import dataclass
from pdip.cqrs import IQuery

from src.application.operation.LookupDataOperation.LookupDataOperationRequest import LookupDataOperationRequest
from src.application.operation.LookupDataOperation.LookupDataOperationResponse import LookupDataOperationResponse


@dataclass
class LookupDataOperationQuery(IQuery[LookupDataOperationResponse]):
    request: LookupDataOperationRequest = None
