from infrastructure.cqrs.decorators.requestclass import requestclass


@requestclass
class CreateDataIntegrationConnectionDatabaseRequest:
    Schema: str = None
    TableName: str = None
    Query: str = None
