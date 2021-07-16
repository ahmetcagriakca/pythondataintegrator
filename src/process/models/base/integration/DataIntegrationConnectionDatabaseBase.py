from models.base.EntityBase import EntityBase
from infrastructure.json.BaseConverter import BaseConverter


@BaseConverter.register
class DataIntegrationConnectionDatabaseBase(EntityBase):

    def __init__(self,
                 DataIntegrationConnectionId: int = None,
                 Schema: str = None,
                 TableName: str = None,
                 Query: str = None,
                 DataIntegrationConnection=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataIntegrationConnectionId: str = DataIntegrationConnectionId
        self.Schema: str = Schema
        self.TableName: str = TableName
        self.Query: str = Query
        self.DataIntegrationConnection = DataIntegrationConnection
