from pdip.cqrs.decorators import dtoclass


@dtoclass
class LookupConnectorTypeDto:
    Id: int = None
    Name: str = None
    ConnectionTypeId: int = None
