from domain.common.decorators.requestclass import requestclass

@requestclass
class CheckDatabaseConnectionRequest:
    ConnectionName: str = None
    Schema: str = None
    Table: str = None
