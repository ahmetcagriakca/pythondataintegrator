from domain.common.decorators.dtoclass import dtoclass


@dtoclass
class GetConnectionDto:
    Id:int =None
    Name:str =None
    ConnectionTypeId:int =None
    ConnectorTypeId:int =None
