from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from pdip.dependency.container import DependencyContainer
from pdip.data import Entity


class DataIntegrationConnectionFileCsv(Entity, DependencyContainer.Base):
    __tablename__ = "DataIntegrationConnectionFileCsv"
    __table_args__ = {"schema": "Integration"}
    DataIntegrationConnectionFileId = Column(Integer, ForeignKey('Integration.DataIntegrationConnectionFile.Id'))
    HasHeader = Column(Boolean, index=False, unique=False, nullable=False)
    Header = Column(String(4000), index=False, unique=False, nullable=True)
    Separator = Column(String(10), index=False, unique=False, nullable=False)
    DataIntegrationConnectionFile = relationship("DataIntegrationConnectionFile", back_populates="Csv")

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
