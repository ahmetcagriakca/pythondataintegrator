from dataclasses import dataclass
from pdip.cqrs import IQuery

from pdi.application.connection.GetConnectionList.GetConnectionListRequest import GetConnectionListRequest
from pdi.application.connection.GetConnectionList.GetConnectionListResponse import GetConnectionListResponse


@dataclass
class GetConnectionListQuery(IQuery[GetConnectionListResponse]):
    request: GetConnectionListRequest = None
