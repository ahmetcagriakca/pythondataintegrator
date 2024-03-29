from typing import List

from pdip.cqrs.decorators import responseclass

from src.application.operation.GetDataOperationJobExecutionIntegrationList.GetDataOperationJobExecutionIntegrationListDto import \
    GetDataOperationJobExecutionIntegrationListDto


@responseclass
class GetDataOperationJobExecutionIntegrationListResponse:
    Data: List[GetDataOperationJobExecutionIntegrationListDto] = None
