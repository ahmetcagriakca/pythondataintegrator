from infrastructor.json.JsonConvert import JsonConvert


@JsonConvert.register
class CreateDataIntegrationConnectionFileModel:
    def __init__(self,
                 FileName: str = None
                 ):
        self.FileName: str = FileName
