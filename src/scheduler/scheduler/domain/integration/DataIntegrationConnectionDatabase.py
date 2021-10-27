from pdip.data import Entity
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from scheduler.domain.base import Base


class DataIntegrationConnectionDatabase(Entity, Base):
    __tablename__ = "DataIntegrationConnectionDatabase"
    __table_args__ = {"schema": "Integration"}
    DataIntegrationConnectionId = Column(Integer, ForeignKey('Integration.DataIntegrationConnection.Id'))
    Schema = Column(String(100), index=False, unique=False, nullable=True)
    TableName = Column(String(100), index=False, unique=False, nullable=True)
    Query = Column(Text, index=False, unique=False, nullable=True)
    DataIntegrationConnection = relationship("DataIntegrationConnection",
                                             back_populates="Database")

    def __init__(self,
                 DataIntegrationConnectionId: int = None,
                 Schema: str = None,
                 TableName: str = None,
                 Query: str = None,
                 DataIntegrationConnection=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataIntegrationConnectionId: str = DataIntegrationConnectionId
        self.Schema: str = Schema
        self.TableName: str = TableName
        self.Query: str = Query
        self.DataIntegrationConnection = DataIntegrationConnection
