from domain.common.decorators.requestclass import requestclass


@requestclass
class CreateConnectionFileRequest:
    Name: str = None
    ConnectorTypeName: int = None
    Host: str = None
    Port: int = None
    User: str = None
    Password: str = None
