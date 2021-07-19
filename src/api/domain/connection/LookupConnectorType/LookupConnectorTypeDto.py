from domain.common.decorators.dtoclass import dtoclass


@dtoclass
class LookupConnectorTypeDto:
    Id:int = None
    Name:str = None
