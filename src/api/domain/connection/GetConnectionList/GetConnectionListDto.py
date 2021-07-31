import datetime
from domain.common.decorators.dtoclass import dtoclass


@dtoclass
class GetConnectionTypeDto:
    Id: int = None
    Name: str = None


@dtoclass
class GetConnectorTypeDto:
    Id: int = None
    Name: str = None


@dtoclass
class GetConnectionListDto:
    Id: int = None
    Name: str = None
    ConnectionType: GetConnectionTypeDto = None
    ConnectorType: GetConnectorTypeDto = None
    Host: str = None
    Port: int = None
    Sid: str = None
    ServiceName: str = None
    DatabaseName: str = None
    CreationDate: datetime.datetime = None
    IsDeleted: int = None
