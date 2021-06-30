from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from IocManager import IocManager
from models.base.integration.DataIntegrationConnectionDatabaseBase import DataIntegrationConnectionDatabaseBase
from models.dao.Entity import Entity


class DataIntegrationConnectionDatabase(DataIntegrationConnectionDatabaseBase,Entity, IocManager.Base):
    __tablename__ = "DataIntegrationConnectionDatabase"
    __table_args__ = {"schema": "Integration"}
    DataIntegrationConnectionId = Column(Integer, ForeignKey('Integration.DataIntegrationConnection.Id'))
    Schema = Column(String(100), index=False, unique=False, nullable=True)
    TableName = Column(String(100), index=False, unique=False, nullable=True)
    Query = Column(Text, index=False, unique=False, nullable=True)
    DataIntegrationConnection = relationship("DataIntegrationConnection",
                                             back_populates="Database")
