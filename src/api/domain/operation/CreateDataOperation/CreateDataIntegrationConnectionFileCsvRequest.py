from infrastructure.cqrs.decorators.requestclass import requestclass


@requestclass
class CreateDataIntegrationConnectionFileCsvRequest:
    HasHeader: bool = None
    Header: str = None
    Separator: str = None