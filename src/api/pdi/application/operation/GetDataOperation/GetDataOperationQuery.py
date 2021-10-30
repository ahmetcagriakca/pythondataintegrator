from dataclasses import dataclass
from pdip.cqrs import IQuery

from pdi.application.operation.GetDataOperation.GetDataOperationRequest import GetDataOperationRequest
from pdi.application.operation.GetDataOperation.GetDataOperationResponse import GetDataOperationResponse


@dataclass
class GetDataOperationQuery(IQuery[GetDataOperationResponse]):
    request: GetDataOperationRequest = None
