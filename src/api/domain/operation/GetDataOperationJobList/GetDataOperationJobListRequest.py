from typing import Optional

from infrastructure.cqrs.decorators.requestclass import requestclass
from domain.common.request_parameter.OrderByParameter import OrderByParameter
from domain.common.request_parameter.PagingParameter import PagingParameter


@requestclass
class GetDataOperationJobListRequest(PagingParameter, OrderByParameter):
    DataOperationId: Optional[int] = None
    DataOperationName: Optional[str] = None
    OnlyCron: Optional[bool] = None
    OnlyUndeleted: Optional[bool] = None