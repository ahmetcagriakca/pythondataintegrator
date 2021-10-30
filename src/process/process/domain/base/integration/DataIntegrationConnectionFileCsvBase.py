from pdip.data import EntityBase


class DataIntegrationConnectionFileCsvBase(EntityBase):
    def __init__(self,
                 DataIntegrationConnectionFileId: int = None,
                 HasHeader: bool = None,
                 Header: str = None,
                 Separator: str = None,
                 DataIntegrationConnectionFile=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataIntegrationConnectionFileId: int = DataIntegrationConnectionFileId
        self.HasHeader: bool = HasHeader
        self.Header: str = Header
        self.Separator: str = Separator
        self.DataIntegrationConnectionFile = DataIntegrationConnectionFile
