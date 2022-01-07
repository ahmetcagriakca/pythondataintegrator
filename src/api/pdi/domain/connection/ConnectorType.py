from typing import List

from pdip.data.domain import Entity
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from pdi.domain.base import Base
from pdi.domain.base.connection.ConnectorTypeBase import ConnectorTypeBase
from pdi.domain.connection.ConnectionBigData import ConnectionBigData
from pdi.domain.connection.ConnectionDatabase import ConnectionDatabase
from pdi.domain.connection.ConnectionFile import ConnectionFile
from pdi.domain.connection.ConnectionQueue import ConnectionQueue


class ConnectorType(ConnectorTypeBase, Entity, Base):
    __tablename__ = "ConnectorType"
    __table_args__ = {"schema": "Connection"}
    ConnectionTypeId = Column(Integer, ForeignKey('Connection.ConnectionType.Id'))
    Name = Column(String(100), index=False, unique=True, nullable=False)
    ConnectionType = relationship("ConnectionType", back_populates="Connectors")
    Databases: List[ConnectionDatabase] = relationship("ConnectionDatabase", back_populates="ConnectorType")
    BigDatas: List[ConnectionBigData] = relationship("ConnectionBigData", back_populates="ConnectorType")
    Files: List[ConnectionFile] = relationship("ConnectionFile", back_populates="ConnectorType")
    Queues: List[ConnectionQueue] = relationship("ConnectionQueue", back_populates="ConnectorType")
