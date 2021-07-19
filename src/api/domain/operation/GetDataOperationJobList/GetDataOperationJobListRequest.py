from typing import Optional

from domain.common.decorators.requestclass import requestclass
from domain.common.request_parameter.OrderByParameter import OrderByParameter
from domain.common.request_parameter.PagingParameter import PagingParameter


@requestclass
class GetDataOperationJobListRequest(PagingParameter, OrderByParameter):
    DataOperationName: Optional[str] = None
    OnlyCron: Optional[bool] = None
    OnlyUndeleted: Optional[bool] = None
