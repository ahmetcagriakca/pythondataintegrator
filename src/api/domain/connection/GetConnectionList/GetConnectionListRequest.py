from typing import Optional

from pdip.cqrs.decorators import requestclass
from domain.common.request_parameter.OrderByParameter import OrderByParameter
from domain.common.request_parameter.PagingParameter import PagingParameter


@requestclass
class GetConnectionListRequest(PagingParameter, OrderByParameter):
    Id: int = None
    ConnectorTypeId: int = None
    ConnectionTypeId: int = None
    OnlyUndeleted: Optional[bool] = None
