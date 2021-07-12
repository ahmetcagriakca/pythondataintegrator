from dataclasses import dataclass
from typing import List

from domain.connection.GetConnectionList.ConnectionListDto import ConnectionListDto
from infrastructor.json.JsonConvert import JsonConvert


@JsonConvert.register
@dataclass
class ConnectionListResponse:
    Connections: List[ConnectionListDto] = None
    PageNumber: int = None
    PageSize: int = None
    Count: int = None

    def to_dict(self):
        return {
            "Connections": [connection.__dict__ for connection in self.Connections],
            "PageNumber": self.PageNumber,
            "PageSize": self.PageSize,
            "Count": self.Count
        }
