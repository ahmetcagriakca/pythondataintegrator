from typing import Optional
from domain.common.decorators.requestclass import requestclass
from domain.common.request_parameter.OrderByParameter import OrderByParameter
from domain.common.request_parameter.PagingParameter import PagingParameter


@requestclass
class GetDataOperationListRequest(PagingParameter, OrderByParameter):
    DataOperationName: Optional[int] = None
    OnlyUndeleted: Optional[bool] = None
