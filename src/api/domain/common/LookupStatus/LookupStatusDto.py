from infrastructure.cqrs.decorators.dtoclass import dtoclass


@dtoclass
class LookupStatusDto:
    Id:int = None
    Name:str = None
