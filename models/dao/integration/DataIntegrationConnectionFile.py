from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity


class DataIntegrationConnectionFile(Entity, IocManager.Base):
    __tablename__ = "DataIntegrationConnectionFile"
    __table_args__ = {"schema": "Integration"}
    DataIntegrationConnectionId = Column(Integer, ForeignKey('Integration.DataIntegrationConnection.Id'))
    FileName = Column(String(1000), index=False, unique=False, nullable=False)
    DataIntegrationConnection = relationship("DataIntegrationConnection", back_populates="File")

    def __init__(self,
                 DataIntegrationConnectionId: int = None,
                 FileName: int = None,
                 DataIntegrationConnection=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataIntegrationConnectionId: int = DataIntegrationConnectionId
        self.FileName: str = FileName
        self.DataIntegrationConnection = DataIntegrationConnection
