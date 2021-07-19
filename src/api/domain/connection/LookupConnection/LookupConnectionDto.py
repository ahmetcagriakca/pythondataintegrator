from domain.common.decorators.dtoclass import dtoclass


@dtoclass
class LookupConnectionDto:
    Id:int = None
    Name:str = None
