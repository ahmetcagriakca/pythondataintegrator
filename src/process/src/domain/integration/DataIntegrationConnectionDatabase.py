from pdip.data.domain import Entity
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from src.domain.base import Base
from src.domain.base.integration.DataIntegrationConnectionDatabaseBase import DataIntegrationConnectionDatabaseBase


class DataIntegrationConnectionDatabase(DataIntegrationConnectionDatabaseBase, Entity, Base):
    __tablename__ = "DataIntegrationConnectionDatabase"
    __table_args__ = {"schema": "Integration"}
    DataIntegrationConnectionId = Column(Integer, ForeignKey('Integration.DataIntegrationConnection.Id'))
    Schema = Column(String(100), index=False, unique=False, nullable=True)
    TableName = Column(String(100), index=False, unique=False, nullable=True)
    Query = Column(Text, index=False, unique=False, nullable=True)
    DataIntegrationConnection = relationship("DataIntegrationConnection",
                                             back_populates="Database")
