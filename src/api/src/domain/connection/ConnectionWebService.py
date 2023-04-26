from pdip.data.domain import Entity
from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.domain.base import Base
from src.domain.base.connection.ConnectionWebServiceBase import ConnectionWebServiceBase
from src.domain.connection.ConnectionWebServiceSoap import ConnectionWebServiceSoap


class ConnectionWebService(ConnectionWebServiceBase, Entity, Base):
    __tablename__ = "ConnectionWebService"
    __table_args__ = {"schema": "Connection"}
    ConnectionId = Column(Integer, ForeignKey('Connection.Connection.Id'))
    ConnectorTypeId = Column(Integer, ForeignKey('Connection.ConnectorType.Id'))
    Ssl = Column(Boolean, index=False, unique=False, nullable=True)
    ConnectorType = relationship("ConnectorType", back_populates="WebServices")
    Soap: ConnectionWebServiceSoap = relationship("ConnectionWebServiceSoap", uselist=False,
                                                  backref="ConnectionWebService")
