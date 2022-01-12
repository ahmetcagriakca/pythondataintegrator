from pdip.data.domain import Entity
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.domain.base import Base
from src.domain.base.integration.DataIntegrationConnectionQueueBase import DataIntegrationConnectionQueueBase


class DataIntegrationConnectionQueue(DataIntegrationConnectionQueueBase, Entity, Base):
    __tablename__ = "DataIntegrationConnectionQueue"
    __table_args__ = {"schema": "Integration"}
    DataIntegrationConnectionId = Column(Integer, ForeignKey('Integration.DataIntegrationConnection.Id'))
    TopicName = Column(String(200), index=False, unique=False, nullable=True)
    DataIntegrationConnection = relationship("DataIntegrationConnection",
                                             back_populates="Queue")
