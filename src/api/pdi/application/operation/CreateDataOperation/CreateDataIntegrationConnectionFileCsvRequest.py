from pdip.cqrs.decorators import requestclass


@requestclass
class CreateDataIntegrationConnectionFileCsvRequest:
    HasHeader: bool = None
    Header: str = None
    Separator: str = None
