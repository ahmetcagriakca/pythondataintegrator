from pdip.data.domain import Entity
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from pdi.domain.base import Base
from pdi.domain.base.integration.DataIntegrationConnectionFileBase import DataIntegrationConnectionFileBase
from pdi.domain.integration.DataIntegrationConnectionFileCsv import DataIntegrationConnectionFileCsv


class DataIntegrationConnectionFile(DataIntegrationConnectionFileBase, Entity, Base):
    __tablename__ = "DataIntegrationConnectionFile"
    __table_args__ = {"schema": "Integration"}
    DataIntegrationConnectionId = Column(Integer, ForeignKey('Integration.DataIntegrationConnection.Id'))
    Folder = Column(String(100), index=False, unique=False, nullable=True)
    FileName = Column(String(1000), index=False, unique=False, nullable=False)
    DataIntegrationConnection = relationship("DataIntegrationConnection", back_populates="File")

    Csv: DataIntegrationConnectionFileCsv = relationship("DataIntegrationConnectionFileCsv", uselist=False,
                                                         back_populates="DataIntegrationConnectionFile")
