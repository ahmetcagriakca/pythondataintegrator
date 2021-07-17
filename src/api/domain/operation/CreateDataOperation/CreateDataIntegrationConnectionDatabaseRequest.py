from domain.common.decorators.requestclass import requestclass


@requestclass
class CreateDataIntegrationConnectionDatabaseRequest:
    Schema: str = None
    TableName: str = None
    Query: str = None
