from pdip.data import Entity
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from scheduler.domain.base import Base


class ConnectionQueue(Entity, Base):
    __tablename__ = "ConnectionQueue"
    __table_args__ = {"schema": "Connection"}
    ConnectionId = Column(Integer, ForeignKey('Connection.Connection.Id'))
    ConnectorTypeId = Column(Integer, ForeignKey('Connection.ConnectorType.Id'))
    Protocol = Column(String(100), index=False, unique=False, nullable=True)
    Mechanism = Column(String(100), index=False, unique=False, nullable=True)
    ConnectorType = relationship("ConnectorType", back_populates="Queues")

    def __init__(self,
                 ConnectionId: int = None,
                 ConnectorTypeId: int = None,
                 Protocol: str = None,
                 Mechanism: str = None,
                 Connection=None,
                 ConnectorType=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ConnectionId: str = ConnectionId
        self.ConnectorTypeId: str = ConnectorTypeId
        self.Protocol: str = Protocol
        self.Mechanism: str = Mechanism
        self.Connection = Connection
        self.ConnectorType = ConnectorType
