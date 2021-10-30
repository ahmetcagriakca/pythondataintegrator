from dataclasses import dataclass
from pdip.cqrs import IQuery

from pdi.application.operation.GetDataOperationJob.GetDataOperationJobRequest import GetDataOperationJobRequest
from pdi.application.operation.GetDataOperationJob.GetDataOperationJobResponse import GetDataOperationJobResponse


@dataclass
class GetDataOperationJobQuery(IQuery[GetDataOperationJobResponse]):
    request: GetDataOperationJobRequest = None
