from dataclasses import dataclass
from pdip.cqrs import IQuery

from src.application.operation.GetDataOperationJobExecutionIntegrationList.GetDataOperationJobExecutionIntegrationListRequest import \
    GetDataOperationJobExecutionIntegrationListRequest
from src.application.operation.GetDataOperationJobExecutionIntegrationList.GetDataOperationJobExecutionIntegrationListResponse import \
    GetDataOperationJobExecutionIntegrationListResponse


@dataclass
class GetDataOperationJobExecutionIntegrationListQuery(IQuery[GetDataOperationJobExecutionIntegrationListResponse]):
    request: GetDataOperationJobExecutionIntegrationListRequest = None