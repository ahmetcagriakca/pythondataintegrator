from dataclasses import dataclass
from typing import List

from domain.connection.GetConnectionList.ConnectionListDto import ConnectionListDto
from infrastructor.json.JsonConvert import JsonConvert


@JsonConvert.register
@dataclass
class ConnectionListResponse:
    PageData: List[ConnectionListDto] = None
    PageNumber: int = None
    PageSize: int = None
    Count: int = None

    def to_dict(self):
        dic = self.__dict__
        dic["PageData"] = [entity.to_dict() for entity in self.PageData]
        return dic
