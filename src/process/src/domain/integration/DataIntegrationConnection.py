from pdip.data.domain import Entity
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.domain.base import Base
from src.domain.base.integration.DataIntegrationConnectionBase import DataIntegrationConnectionBase
from src.domain.integration.DataIntegrationConnectionBigData import DataIntegrationConnectionBigData
from src.domain.integration.DataIntegrationConnectionDatabase import DataIntegrationConnectionDatabase
from src.domain.integration.DataIntegrationConnectionFile import DataIntegrationConnectionFile
from src.domain.integration.DataIntegrationConnectionQueue import DataIntegrationConnectionQueue


class DataIntegrationConnection(DataIntegrationConnectionBase, Entity, Base):
    __tablename__ = "DataIntegrationConnection"
    __table_args__ = {"schema": "Integration"}
    DataIntegrationId = Column(Integer, ForeignKey('Integration.DataIntegration.Id'))
    ConnectionId = Column(Integer, ForeignKey('Connection.Connection.Id'))
    SourceOrTarget = Column(Integer, index=False, unique=False, nullable=False)
    Connection = relationship("Connection", back_populates="DataIntegrationConnections")
    DataIntegration = relationship("DataIntegration", back_populates="Connections")
    Database: DataIntegrationConnectionDatabase = relationship("DataIntegrationConnectionDatabase", uselist=False,
                                                               back_populates="DataIntegrationConnection")
    BigData: DataIntegrationConnectionBigData = relationship("DataIntegrationConnectionBigData", uselist=False,
                                                               back_populates="DataIntegrationConnection")
    File: DataIntegrationConnectionFile = relationship("DataIntegrationConnectionFile", uselist=False,
                                                       back_populates="DataIntegrationConnection")
    Queue: DataIntegrationConnectionQueue = relationship("DataIntegrationConnectionQueue", uselist=False,
                                                         back_populates="DataIntegrationConnection")
