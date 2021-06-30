from sqlalchemy import Column, String, Integer, Text, Boolean
from sqlalchemy.orm import relationship
from IocManager import IocManager
from models.base.operation.DefinitionBase import DefinitionBase
from models.dao.Entity import Entity


class Definition(DefinitionBase, Entity, IocManager.Base):
    __tablename__ = "Definition"
    __table_args__ = {"schema": "Operation"}
    Name = Column(String(100), index=False, unique=False, nullable=False)
    Version = Column(Integer, index=False, unique=False, nullable=False)
    Content = Column(Text, index=False, unique=False, nullable=True)
    IsActive = Column(Boolean, index=False, unique=False, nullable=False)

    DataOperations = relationship("DataOperation", back_populates="Definition")
    DataIntegrations = relationship("DataIntegration", back_populates="Definition")
    DataOperationJobExecutions = relationship("DataOperationJobExecution", back_populates="Definition")
