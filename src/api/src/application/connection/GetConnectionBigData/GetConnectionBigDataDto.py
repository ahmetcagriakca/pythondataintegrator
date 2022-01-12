import datetime

from pdip.cqrs.decorators import dtoclass


@dtoclass
class GetConnectionTypeDto:
    Id: int = None
    Name: str = None


@dtoclass
class GetAuthenticationTypeDto:
    Id: int = None
    Name: str = None


@dtoclass
class GetConnectorTypeDto:
    Id: int = None
    Name: str = None
    ConnectionTypeId: int = None


@dtoclass
class GetConnectionBigDataDto:
    Id: int = None
    Name: str = None
    ConnectionType: GetConnectionTypeDto = None
    ConnectorType: GetConnectorTypeDto = None
    Host: str = None
    Port: int = None
    DatabaseName: str = None
    AuthenticationType: GetAuthenticationTypeDto = None
    KrbRealm: str = None
    KrbFqdn: str = None
    KrbServiceName: str = None
    Ssl: bool = None
    UseOnlySspi: bool = None
    CreationDate: datetime.datetime = None
    IsDeleted: int = None
