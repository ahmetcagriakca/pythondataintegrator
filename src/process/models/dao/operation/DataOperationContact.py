from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.dao.base import Base
from models.base.operation.DataOperationContactBase import DataOperationContactBase
from pdip.data import Entity


class DataOperationContact(DataOperationContactBase, Entity, Base):
    __tablename__ = "DataOperationContact"
    __table_args__ = {"schema": "Operation"}
    DataOperationId = Column(Integer, ForeignKey('Operation.DataOperation.Id'))
    Email = Column(String(250), index=False, unique=False, nullable=False)
    DataOperation = relationship("DataOperation", back_populates="Contacts")