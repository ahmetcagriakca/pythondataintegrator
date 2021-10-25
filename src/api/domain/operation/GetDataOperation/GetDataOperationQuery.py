from dataclasses import dataclass
from pdip.cqrs import IQuery
from domain.operation.GetDataOperation.GetDataOperationRequest import GetDataOperationRequest
from domain.operation.GetDataOperation.GetDataOperationResponse import GetDataOperationResponse


@dataclass
class GetDataOperationQuery(IQuery[GetDataOperationResponse]):
    request: GetDataOperationRequest = None
