from dataclasses import dataclass

from domain.connection.GetConnectionList.GetConnectionListRequest import GetConnectionListRequest
from domain.connection.GetConnectionList.GetConnectionListResponse import GetConnectionListResponse
from infrastructor.cqrs.IQuery import IQuery


@dataclass
class GetConnectionListQuery(IQuery[GetConnectionListResponse]):
    request: GetConnectionListRequest= None
