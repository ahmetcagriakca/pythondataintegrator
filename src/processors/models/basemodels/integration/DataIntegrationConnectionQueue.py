from infrastructor.json.JsonConvert import JsonConvert
from models.basemodels.integration import DataIntegrationConnectionFileCsv


@JsonConvert.register
class DataIntegrationConnectionQueue:
    def __init__(self,
                 TopicName: str = None,
                 ):
        self.TopicName: str = TopicName
