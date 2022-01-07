from pdip.cqrs.decorators import dtoclass


@dtoclass
class LookupConnectionTypeDto:
    Id: int = None
    Name: str = None
