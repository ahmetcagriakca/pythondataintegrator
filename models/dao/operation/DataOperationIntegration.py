from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity


class DataOperationIntegration(Entity, IocManager.Base):
    __tablename__ = "DataOperationIntegration"
    __table_args__ = {"schema": "Operation"}
    DataOperationId = Column(Integer, ForeignKey('Operation.DataOperation.Id'))
    PythonDataIntegrationId = Column(Integer, ForeignKey('Integration.PythonDataIntegration.Id'))
    Order = Column(Integer, index=False, unique=False, nullable=False)
    SourceCount = Column(Integer, index=False, unique=False, nullable=True)
    DataOperation = relationship("DataOperation", back_populates="Integrations")
    PythonDataIntegration = relationship("PythonDataIntegration", back_populates="DataOperationIntegrations")

    def __init__(self,
                 DataOperationId: int = None,
                 PythonDataIntegrationId: int = None,
                 Order: int = None,
                 SourceCount: int = None,
                 DataOperation = None,
                 PythonDataIntegration = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataOperationId: int = DataOperationId
        self.PythonDataIntegrationId: int = PythonDataIntegrationId
        self.Order: int = Order
        self.SourceCount: int = SourceCount
        self.DataOperation = DataOperation
        self.PythonDataIntegration = PythonDataIntegration
