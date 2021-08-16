from dataclasses import dataclass
from infrastructure.cqrs.IQuery import IQuery
from domain.operation.GetDataOperationJob.GetDataOperationJobRequest import GetDataOperationJobRequest
from domain.operation.GetDataOperationJob.GetDataOperationJobResponse import GetDataOperationJobResponse


@dataclass
class GetDataOperationJobQuery(IQuery[GetDataOperationJobResponse]):
    request: GetDataOperationJobRequest = None
