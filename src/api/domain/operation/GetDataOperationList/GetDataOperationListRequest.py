from typing import Optional
from pdip.cqrs.decorators import requestclass
from pdip.api.request_parameter import OrderByParameter
from pdip.api.request_parameter import PagingParameter


@requestclass
class GetDataOperationListRequest(PagingParameter, OrderByParameter):
    DataOperationName: Optional[str] = None
    OnlyUndeleted: Optional[bool] = None
