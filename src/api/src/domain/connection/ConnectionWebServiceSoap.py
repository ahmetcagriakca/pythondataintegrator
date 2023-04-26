from pdip.data.domain import Entity
from sqlalchemy import Column, String, Integer, ForeignKey

from src.domain.base import Base
from src.domain.base.connection.ConnectionWebServiceSoapBase import ConnectionWebServiceSoapBase


class ConnectionWebServiceSoap(ConnectionWebServiceSoapBase, Entity, Base):
    __tablename__ = "ConnectionWebServiceSoap"
    __table_args__ = {"schema": "Connection"}
    ConnectionWebServiceId = Column(Integer, ForeignKey('Connection.ConnectionWebService.Id'))
    Wsdl = Column(String(500), index=False, unique=False, nullable=True)
