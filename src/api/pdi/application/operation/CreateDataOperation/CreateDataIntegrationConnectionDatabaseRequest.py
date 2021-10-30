from pdip.cqrs.decorators import requestclass


@requestclass
class CreateDataIntegrationConnectionDatabaseRequest:
    Schema: str = None
    TableName: str = None
    Query: str = None
