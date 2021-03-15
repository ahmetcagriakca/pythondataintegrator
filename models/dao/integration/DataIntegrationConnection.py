from typing import List

from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity
from models.dao.integration.DataIntegrationConnectionDatabase import DataIntegrationConnectionDatabase
from models.dao.integration.DataIntegrationConnectionFile import DataIntegrationConnectionFile


class DataIntegrationConnection(Entity, IocManager.Base):
    __tablename__ = "DataIntegrationConnection"
    __table_args__ = {"schema": "Integration"}
    DataIntegrationId = Column(Integer, ForeignKey('Integration.DataIntegration.Id'))
    ConnectionId = Column(Integer, ForeignKey('Connection.Connection.Id'))
    SourceOrTarget = Column(Integer, index=False, unique=False, nullable=False)
    Connection = relationship("Connection", back_populates="DataIntegrationConnections")
    DataIntegration = relationship("DataIntegration", back_populates="Connections")
    File: DataIntegrationConnectionFile = relationship("DataIntegrationConnectionFile", uselist=False,
                                                             back_populates="DataIntegrationConnection")
    Database: DataIntegrationConnectionDatabase = relationship("DataIntegrationConnectionDatabase", uselist=False,
                                                                     back_populates="DataIntegrationConnection")

    def __init__(self,
                 SourceOrTarget: int = None,
                 DataIntegrationId: int = None,
                 ConnectionId: int = None,
                 Schema: str = None,
                 TableName: str = None,
                 Query: str = None,
                 DataIntegration=None,
                 Connection=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SourceOrTarget: int = SourceOrTarget
        self.DataIntegrationId: str = DataIntegrationId
        self.ConnectionId: str = ConnectionId
        self.Schema: str = Schema
        self.TableName: str = TableName
        self.Query: str = Query
        self.DataIntegration = DataIntegration
        self.Connection = Connection
