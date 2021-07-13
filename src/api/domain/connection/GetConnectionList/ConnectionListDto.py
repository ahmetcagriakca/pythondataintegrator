import datetime
from dataclasses import dataclass

from infrastructor.json.JsonConvert import JsonConvert


@JsonConvert.register
@dataclass
class ConnectionListDto:
    Id: int = None
    Name: int = None
    ConnectorTypeId: int = None
    ConnectorTypeName: str = None
    ConnectionTypeId: int = None
    ConnectionTypeName: str = None
    Host: str = None
    Port: int = None
    Sid: str = None
    ServiceName: str = None
    DatabaseName: str = None
    CreationDate: datetime.datetime = None

    def to_dict(self):
        dic = self.__dict__
        return dic
