from pdip.cqrs.decorators import requestclass


@requestclass
class CreateConnectionBigDataRequest:
    Name: str = None
    ConnectorTypeId: int = None
    AuthenticationType: int = None
    Host: str = None
    Port: int = None
    DatabaseName: str = None
    User: str = None
    Password: str = None
    KrbRealm: str = None
    KrbFqdn: str = None
    KrbServiceName: str = None
    Ssl: bool = None
    UseOnlySspi: bool = None
