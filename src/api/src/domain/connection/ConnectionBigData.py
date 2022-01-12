from pdip.data.domain import Entity
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.domain.base import Base
from src.domain.base.connection.ConnectionBigDataBase import ConnectionBigDataBase


class ConnectionBigData(ConnectionBigDataBase, Entity, Base):
    __tablename__ = "ConnectionBigData"
    __table_args__ = {"schema": "Connection"}
    ConnectionId = Column(Integer, ForeignKey('Connection.Connection.Id'))
    ConnectorTypeId = Column(Integer, ForeignKey('Connection.ConnectorType.Id'))
    DatabaseName = Column(String(100), index=False, unique=False, nullable=True)
    Ssl = Column(Boolean, index=False, unique=False, nullable=True)
    UseOnlySspi = Column(Boolean, index=False, unique=False, nullable=True)
    ConnectorType = relationship("ConnectorType", back_populates="BigDatas")
