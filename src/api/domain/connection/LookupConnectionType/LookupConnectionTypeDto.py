from domain.common.decorators.dtoclass import dtoclass


@dtoclass
class LookupConnectionTypeDto:
    Id:int = None
    Name:str = None
