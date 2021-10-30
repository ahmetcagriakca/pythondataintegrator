from typing import Optional

from pdip.api.request_parameter import OrderByParameter
from pdip.api.request_parameter import PagingParameter
from pdip.cqrs.decorators import requestclass


@requestclass
class GetDataOperationListRequest(PagingParameter, OrderByParameter):
    DataOperationName: Optional[str] = None
    OnlyUndeleted: Optional[bool] = None
