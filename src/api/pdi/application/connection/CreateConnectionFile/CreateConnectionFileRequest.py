from pdip.cqrs.decorators import requestclass


@requestclass
class CreateConnectionFileRequest:
    Name: str = None
    ConnectorTypeName: str = None
    Host: str = None
    Port: int = None
    User: str = None
    Password: str = None
