from typing import Optional

from infrastructure.cqrs.decorators.requestclass import requestclass
from domain.common.request_parameter.OrderByParameter import OrderByParameter
from domain.common.request_parameter.PagingParameter import PagingParameter


@requestclass
class GetConnectionListRequest(PagingParameter, OrderByParameter):
    Id: int = None
    ConnectorTypeId: int = None
    ConnectionTypeId: int = None
    OnlyUndeleted: Optional[bool] = None
