from dataclasses import dataclass

from domain.connection.GetConnectionList.GetConnectionListRequest import GetConnectionListRequest


@dataclass
class GetConnectionListQuery:
    request: GetConnectionListRequest= None
