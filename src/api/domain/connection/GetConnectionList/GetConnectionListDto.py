import datetime
from domain.common.decorators.dtoclass import dtoclass


@dtoclass
class GetConnectionListDto:
    Id: int = None
    Name: str = None
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

