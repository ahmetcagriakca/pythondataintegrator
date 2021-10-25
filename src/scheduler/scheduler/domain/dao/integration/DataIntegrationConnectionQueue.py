from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from pdip.dependency.container import DependencyContainer
from scheduler.domain.dao.Entity import Entity


class DataIntegrationConnectionQueue(Entity, DependencyContainer.Base):
    __tablename__ = "DataIntegrationConnectionQueue"
    __table_args__ = {"schema": "Integration"}
    DataIntegrationConnectionId = Column(Integer, ForeignKey('Integration.DataIntegrationConnection.Id'))
    TopicName = Column(String(200), index=False, unique=False, nullable=True)
    DataIntegrationConnection = relationship("DataIntegrationConnection",
                                             back_populates="Queue")

    def __init__(self,
                 DataIntegrationConnectionId: int = None,
                 TopicName: str = None,
                 DataIntegrationConnection=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataIntegrationConnectionId: str = DataIntegrationConnectionId
        self.TopicName: str = TopicName
        self.DataIntegrationConnection = DataIntegrationConnection
