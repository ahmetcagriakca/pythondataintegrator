from dataclasses import dataclass
from pdip.cqrs import IQuery

from src.application.operation.GetDataOperation.GetDataOperationRequest import GetDataOperationRequest
from src.application.operation.GetDataOperation.GetDataOperationResponse import GetDataOperationResponse


@dataclass
class GetDataOperationQuery(IQuery[GetDataOperationResponse]):
    request: GetDataOperationRequest = None
