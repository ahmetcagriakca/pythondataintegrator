from pdip.cqrs.decorators import dtoclass


@dtoclass
class LookupConnectionDto:
    Id: int = None
    Name: str = None
    ConnectionTypeId: int = None
    IsDeleted: int = None
