from pdip.data.domain import Entity
from sqlalchemy import Column, String, Integer, Text, Boolean
from sqlalchemy.orm import relationship

from src.domain.base import Base
from src.domain.base.operation.DefinitionBase import DefinitionBase


class Definition(DefinitionBase, Entity, Base):
    __tablename__ = "Definition"
    __table_args__ = {"schema": "Operation"}
    Name = Column(String(100), index=False, unique=False, nullable=False)
    Version = Column(Integer, index=False, unique=False, nullable=False)
    Content = Column(Text, index=False, unique=False, nullable=True)
    IsActive = Column(Boolean, index=False, unique=False, nullable=False)

    DataOperations = relationship("DataOperation", back_populates="Definition")
    DataIntegrations = relationship("DataIntegration", back_populates="Definition")
    DataOperationJobExecutions = relationship("DataOperationJobExecution", back_populates="Definition")
