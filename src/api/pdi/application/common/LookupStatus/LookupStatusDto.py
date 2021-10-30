from pdip.cqrs.decorators import dtoclass


@dtoclass
class LookupStatusDto:
    Id: int = None
    Name: str = None
