from models.base.EntityBase import EntityBase
from infrastructor.json.BaseConverter import BaseConverter


@BaseConverter.register
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
