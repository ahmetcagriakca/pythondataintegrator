from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from pdip.dependency.container import DependencyContainer
from pdip.data import Entity
from models.dao.integration.DataIntegrationConnectionFileCsv import DataIntegrationConnectionFileCsv


class DataIntegrationConnectionFile(Entity, DependencyContainer.Base):
    __tablename__ = "DataIntegrationConnectionFile"
    __table_args__ = {"schema": "Integration"}
    DataIntegrationConnectionId = Column(Integer, ForeignKey('Integration.DataIntegrationConnection.Id'))
    Folder = Column(String(100), index=False, unique=False, nullable=True)
    FileName = Column(String(1000), index=False, unique=False, nullable=False)
    DataIntegrationConnection = relationship("DataIntegrationConnection", back_populates="File")

    Csv: DataIntegrationConnectionFileCsv = relationship("DataIntegrationConnectionFileCsv", uselist=False,
                                                         back_populates="DataIntegrationConnectionFile")

    def __init__(self,
                 DataIntegrationConnectionId: int = None,
                 Folder: str = None,
                 FileName: str = None,
                 DataIntegrationConnection=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataIntegrationConnectionId: int = DataIntegrationConnectionId
        self.Folder: str = Folder
        self.FileName: str = FileName
        self.DataIntegrationConnection = DataIntegrationConnection
