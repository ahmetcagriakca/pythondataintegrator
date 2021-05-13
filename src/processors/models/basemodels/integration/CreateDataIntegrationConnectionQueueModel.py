from infrastructor.json.JsonConvert import JsonConvert
from models.viewmodels.integration import DataIntegrationConnectionFileCsv


@JsonConvert.register
class CreateDataIntegrationConnectionQueueModel:
    def __init__(self,
                 TopicName: str = None,
                 ):
        self.TopicName: str = TopicName
