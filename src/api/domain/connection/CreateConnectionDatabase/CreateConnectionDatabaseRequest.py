from infrastructure.cqrs.decorators.requestclass import requestclass


@requestclass
class CreateConnectionDatabaseRequest:
    Name: str = None
    ConnectorTypeName: str = None
    Host: str = None
    Port: int = None
    Sid: str = None
    ServiceName: str = None
    DatabaseName: str = None
    User: str = None
    Password: str = None
