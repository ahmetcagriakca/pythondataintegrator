from infrastructure.cqrs.decorators.dtoclass import dtoclass


@dtoclass
class LookupConnectionDto:
    Id: int = None
    Name: str = None
    ConnectionTypeId: int = None
    IsDeleted: int = None
