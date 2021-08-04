from typing import Optional

from domain.common.decorators.requestclass import requestclass
from domain.common.request_parameter.OrderByParameter import OrderByParameter
from domain.common.request_parameter.PagingParameter import PagingParameter


@requestclass
class GetDataOperationJobExecutionListRequest(PagingParameter, OrderByParameter):
    DataOperationId: Optional[int] = None
    DataOperationJobId: Optional[int] = None
    DataOperationName: Optional[str] = None
    OnlyCron: Optional[bool] = None
    StatusId: Optional[int] = None
