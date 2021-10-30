from typing import List

from pdip.cqrs.decorators import requestclass


@requestclass
class CreateConnectionServerRequest:
    Host: str = None
    Port: int = None


@requestclass
class CreateConnectionQueueRequest:
    Name: str = None
    ConnectorTypeName: str = None
    Servers: List[CreateConnectionServerRequest] = None
    Protocol: str = None
    Mechanism: str = None
    User: str = None
    Password: str = None
