from typing import List

from pdip.cqrs.decorators import responseclass

from pdi.application.operation.GetDataOperationJobExecutionLogList.GetDataOperationJobExecutionLogListDto import \
    GetDataOperationJobExecutionLogListDto


@responseclass
class GetDataOperationJobExecutionLogListResponse:
    Data: List[GetDataOperationJobExecutionLogListDto] = None
