from typing import Optional

from pdip.api.request_parameter import OrderByParameter
from pdip.api.request_parameter import PagingParameter
from pdip.cqrs.decorators import requestclass


@requestclass
class GetDataOperationJobListRequest(PagingParameter, OrderByParameter):
    DataOperationId: Optional[int] = None
    DataOperationName: Optional[str] = None
    OnlyCron: Optional[bool] = None
    OnlyUndeleted: Optional[bool] = None
