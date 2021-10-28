from pdip.data import Entity
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from process.domain.base import Base
from process.domain.base.operation.DataOperationContactBase import DataOperationContactBase


class DataOperationContact(DataOperationContactBase, Entity, Base):
    __tablename__ = "DataOperationContact"
    __table_args__ = {"schema": "Operation"}
    DataOperationId = Column(Integer, ForeignKey('Operation.DataOperation.Id'))
    Email = Column(String(250), index=False, unique=False, nullable=False)
    DataOperation = relationship("DataOperation", back_populates="Contacts")
