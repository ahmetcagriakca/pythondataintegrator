from pdip.api.request_parameter import OrderByParameter
from pdip.api.request_parameter import PagingParameter
from pdip.cqrs.decorators import requestclass


@requestclass
class GetConnectionListRequest(PagingParameter, OrderByParameter):
    Id: int = None
    ConnectorTypeId: int = None
    ConnectionTypeId: int = None
    OnlyUndeleted: bool = None
