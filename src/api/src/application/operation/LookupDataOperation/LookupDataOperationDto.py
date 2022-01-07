from pdip.cqrs.decorators import dtoclass


@dtoclass
class LookupDataOperationDto:
    Id: int = None
    Name: str = None
    IsDeleted: int = None
