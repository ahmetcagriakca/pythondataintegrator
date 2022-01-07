from dataclasses import dataclass
from pdip.cqrs import IQuery

from src.application.connection.GetConnectionList.GetConnectionListRequest import GetConnectionListRequest
from src.application.connection.GetConnectionList.GetConnectionListResponse import GetConnectionListResponse


@dataclass
class GetConnectionListQuery(IQuery[GetConnectionListResponse]):
    request: GetConnectionListRequest = None
