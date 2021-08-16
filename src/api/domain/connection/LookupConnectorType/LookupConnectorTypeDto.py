from infrastructure.cqrs.decorators.dtoclass import dtoclass


@dtoclass
class LookupConnectorTypeDto:
    Id: int = None
    Name: str = None
    ConnectionTypeId: int = None