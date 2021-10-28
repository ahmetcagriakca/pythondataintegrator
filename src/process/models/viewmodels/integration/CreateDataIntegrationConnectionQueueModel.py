from pdip.json import JsonConvert
from models.viewmodels.integration import CreateDataIntegrationConnectionFileCsvModel


@JsonConvert.register
class CreateDataIntegrationConnectionQueueModel:
    def __init__(self,
                 TopicName: str = None,
                 ):
        self.TopicName: str = TopicName
