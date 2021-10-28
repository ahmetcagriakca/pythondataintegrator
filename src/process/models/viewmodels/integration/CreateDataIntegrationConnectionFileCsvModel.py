from pdip.json import JsonConvert


@JsonConvert.register
class CreateDataIntegrationConnectionFileModel:
    def __init__(self,
                 HasHeader: bool = None,
                 Header: str = None,
                 Separator: str = None,
                 ):
        self.HasHeader: bool  = HasHeader
        self.Header: str = Header
        self.Separator: str = Separator
