from dataclasses import dataclass
from pdip.cqrs import IQuery

from src.application.operation.GetDataOperationJob.GetDataOperationJobRequest import GetDataOperationJobRequest
from src.application.operation.GetDataOperationJob.GetDataOperationJobResponse import GetDataOperationJobResponse


@dataclass
class GetDataOperationJobQuery(IQuery[GetDataOperationJobResponse]):
    request: GetDataOperationJobRequest = None
