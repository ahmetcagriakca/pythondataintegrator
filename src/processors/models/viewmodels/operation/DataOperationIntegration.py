from infrastructor.json.JsonConvert import JsonConvert
from models.viewmodels.integration.DataIntegration import DataIntegration


@JsonConvert.register
class DataOperationIntegration:
    def __init__(self,
                 Limit: int = None,
                 ProcessCount: int = None,
                 Integration: DataIntegration = None,
                 *args, **kwargs):
        self.Limit: int = Limit
        self.ProcessCount: int = ProcessCount
        self.Integration: DataIntegration = Integration
