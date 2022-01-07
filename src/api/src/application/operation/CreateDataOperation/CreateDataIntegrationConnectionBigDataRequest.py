from pdip.cqrs.decorators import requestclass


@requestclass
class CreateDataIntegrationConnectionBigDataRequest:
    Schema: str = None
    TableName: str = None
    Query: str = None
