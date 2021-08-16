from dataclasses import dataclass
from infrastructure.cqrs.IQuery import IQuery
from domain.operation.LookupDataOperation.LookupDataOperationRequest import LookupDataOperationRequest
from domain.operation.LookupDataOperation.LookupDataOperationResponse import LookupDataOperationResponse


@dataclass
class LookupDataOperationQuery(IQuery[LookupDataOperationResponse]):
    request: LookupDataOperationRequest = None
