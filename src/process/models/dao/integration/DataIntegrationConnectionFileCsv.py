from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from IocManager import IocManager
from models.base.integration.DataIntegrationConnectionFileCsvBase import DataIntegrationConnectionFileCsvBase
from models.dao.Entity import Entity


class DataIntegrationConnectionFileCsv(DataIntegrationConnectionFileCsvBase,Entity, IocManager.Base):
    __tablename__ = "DataIntegrationConnectionFileCsv"
    __table_args__ = {"schema": "Integration"}
    DataIntegrationConnectionFileId = Column(Integer, ForeignKey('Integration.DataIntegrationConnectionFile.Id'))
    HasHeader = Column(Boolean, index=False, unique=False, nullable=False)
    Header = Column(String(4000), index=False, unique=False, nullable=True)
    Separator = Column(String(10), index=False, unique=False, nullable=False)
    DataIntegrationConnectionFile = relationship("DataIntegrationConnectionFile", back_populates="Csv")
