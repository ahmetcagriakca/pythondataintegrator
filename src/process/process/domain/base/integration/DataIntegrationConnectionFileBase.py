from pdip.data import EntityBase

from process.domain.base.integration.DataIntegrationConnectionFileCsvBase import DataIntegrationConnectionFileCsvBase


class DataIntegrationConnectionFileBase(EntityBase):

    def __init__(self,
                 DataIntegrationConnectionId: int = None,
                 Folder: str = None,
                 FileName: str = None,
                 DataIntegrationConnection=None,
                 Csv: DataIntegrationConnectionFileCsvBase = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataIntegrationConnectionId: int = DataIntegrationConnectionId
        self.Folder: str = Folder
        self.FileName: str = FileName
        self.DataIntegrationConnection = DataIntegrationConnection
        self.Csv = Csv
