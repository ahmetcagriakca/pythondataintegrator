from pdip.data.domain import Entity
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.domain.base import Base
from src.domain.base.integration.DataIntegrationConnectionFileCsvBase import DataIntegrationConnectionFileCsvBase


class DataIntegrationConnectionFileCsv(DataIntegrationConnectionFileCsvBase, Entity, Base):
    __tablename__ = "DataIntegrationConnectionFileCsv"
    __table_args__ = {"schema": "Integration"}
    DataIntegrationConnectionFileId = Column(Integer, ForeignKey('Integration.DataIntegrationConnectionFile.Id'))
    HasHeader = Column(Boolean, index=False, unique=False, nullable=False)
    Header = Column(String(4000), index=False, unique=False, nullable=True)
    Separator = Column(String(10), index=False, unique=False, nullable=False)
    DataIntegrationConnectionFile = relationship("DataIntegrationConnectionFile", back_populates="Csv")
