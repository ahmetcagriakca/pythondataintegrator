from infrastructure.cqrs.decorators.dtoclass import dtoclass


@dtoclass
class LookupDataOperationDto:
    Id:int = None
    Name:str = None
