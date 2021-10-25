from typing import Optional
from pdip.cqrs.decorators import requestclass
from domain.common.request_parameter.OrderByParameter import OrderByParameter
from domain.common.request_parameter.PagingParameter import PagingParameter


@requestclass
class GetDataOperationListRequest(PagingParameter, OrderByParameter):
    DataOperationName: Optional[str] = None
    OnlyUndeleted: Optional[bool] = None
