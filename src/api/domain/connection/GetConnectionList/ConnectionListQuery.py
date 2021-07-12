from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from domain.connection.GetConnectionList.ConnectionListRequest import ConnectionListRequest


@dataclass
class ConnectionListQuery:
    ConnectionListRequest: ConnectionListRequest= None
