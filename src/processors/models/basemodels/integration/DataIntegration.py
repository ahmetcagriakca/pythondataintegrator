from models.basemodels.integration.DataIntegrationConnection import DataIntegrationConnection
from infrastructor.json.JsonConvert import JsonConvert


@JsonConvert.register
class DataIntegration:
    def __init__(self,
                 Code: str = None,
                 SourceConnections: DataIntegrationConnection = None,
                 TargetConnections: DataIntegrationConnection = None,
                 IsTargetTruncate: bool = None,
                 IsDelta: bool = None,
                 Comments: str = None,
                 ):
        self.Code: str = Code
        self.SourceConnections: DataIntegrationConnection = SourceConnections
        self.TargetConnections: DataIntegrationConnection = TargetConnections
        self.IsTargetTruncate: bool = IsTargetTruncate
        self.IsDelta = IsDelta
        self.Comments: str = Comments
