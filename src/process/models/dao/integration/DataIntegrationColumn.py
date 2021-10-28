from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.dao.base import Base
from models.base.integration.DataIntegrationColumnBase import DataIntegrationColumnBase
from pdip.data import Entity


class DataIntegrationColumn(DataIntegrationColumnBase, Entity, Base):
    __tablename__ = "DataIntegrationColumn"
    __table_args__ = {"schema": "Integration"}
    DataIntegrationId = Column(Integer, ForeignKey('Integration.DataIntegration.Id'))
    ResourceType = Column(String(100), index=False, unique=False, nullable=True)
    SourceColumnName = Column(String(100), index=False, unique=False, nullable=True)
    TargetColumnName = Column(String(100), index=False, unique=False, nullable=True)
    DataIntegration = relationship("DataIntegration", back_populates="Columns")
