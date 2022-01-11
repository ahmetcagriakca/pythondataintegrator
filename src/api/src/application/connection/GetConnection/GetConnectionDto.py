import datetime

from pdip.cqrs.decorators import dtoclass


@dtoclass
class GetConnectionTypeDto:
    Id: int = None
    Name: str = None


@dtoclass
class GetConnectionDto:
    Id: int = None
    Name: str = None
    ConnectionType: GetConnectionTypeDto = None
    CreationDate: datetime.datetime = None
    IsDeleted: int = None
