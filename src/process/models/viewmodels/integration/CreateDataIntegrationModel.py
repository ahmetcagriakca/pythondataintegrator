from models.viewmodels.integration.CreateDataIntegrationConnectionModel import CreateDataIntegrationConnectionModel
from pdip.json import JsonConvert


@JsonConvert.register
class CreateDataIntegrationModel:
    def __init__(self,
                 Code: str = None,
                 SourceConnections: CreateDataIntegrationConnectionModel = None,
                 TargetConnections: CreateDataIntegrationConnectionModel = None,
                 IsTargetTruncate: bool = None,
                 IsDelta: bool = None,
                 Comments: str = None,
                 ):
        self.Code: str = Code
        self.SourceConnections: CreateDataIntegrationConnectionModel = SourceConnections
        self.TargetConnections: CreateDataIntegrationConnectionModel = TargetConnections
        self.IsTargetTruncate: bool = IsTargetTruncate
        self.IsDelta = IsDelta
        self.Comments: str = Comments
