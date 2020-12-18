from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity


class PythonDataIntegrationConnection(Entity, IocManager.Base):
    __tablename__ = "PythonDataIntegrationConnection"
    __table_args__ = {"schema": "Integration"}
    PythonDataIntegrationId = Column(Integer, ForeignKey('Integration.PythonDataIntegration.Id'))
    ConnectionId = Column(Integer, ForeignKey('Connection.Connection.Id'))
    SourceOrTarget = Column(Integer, index=False, unique=False, nullable=False)
    Schema = Column(String(100), index=False, unique=False, nullable=True)
    TableName = Column(String(100), index=False, unique=False, nullable=True)
    Connection = relationship("Connection", back_populates="PythonDataIntegrationConnections")
    PythonDataIntegration = relationship("PythonDataIntegration", back_populates="Connections")

    def __init__(self,
                 SourceOrTarget: int = None,
                 PythonDataIntegrationId: int = None,
                 ConnectionId: int = None,
                 Schema: str = None,
                 TableName: str = None,
                 PythonDataIntegration=None,
                 Connection=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SourceOrTarget: int = SourceOrTarget
        self.PythonDataIntegrationId: str = PythonDataIntegrationId
        self.ConnectionId: str = ConnectionId
        self.Schema: str = Schema
        self.TableName: str = TableName
        self.PythonDataIntegration = PythonDataIntegration
        self.Connection = Connection
