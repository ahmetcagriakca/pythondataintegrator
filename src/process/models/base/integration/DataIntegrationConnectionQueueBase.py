from models.base.EntityBase import EntityBase
from infrastructure.json.BaseConverter import BaseConverter


@BaseConverter.register
class DataIntegrationConnectionQueueBase(EntityBase):

    def __init__(self,
                 DataIntegrationConnectionId: int = None,
                 TopicName: str = None,
                 DataIntegrationConnection=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataIntegrationConnectionId: str = DataIntegrationConnectionId
        self.TopicName: str = TopicName
        self.DataIntegrationConnection = DataIntegrationConnection
