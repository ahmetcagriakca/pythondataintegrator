from pdip.cqrs.decorators import requestclass


@requestclass
class CreateConnectionWebServiceSoap:
    Wsdl: str = None


@requestclass
class CreateConnectionWebServiceRequest:
    Name: str = None
    ConnectorTypeId: int = None
    Host: str = None
    Port: int = None
    User: str = None
    Password: str = None
    Ssl: bool = None
    Soap: CreateConnectionWebServiceSoap = None
