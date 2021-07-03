from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from IocManager import IocManager
from models.base.operation.DataOperationContactBase import DataOperationContactBase
from models.dao.Entity import Entity


class DataOperationContact(DataOperationContactBase,Entity, IocManager.Base):
    __tablename__ = "DataOperationContact"
    __table_args__ = {"schema": "Operation"}
    DataOperationId = Column(Integer, ForeignKey('Operation.DataOperation.Id'))
    Email = Column(String(250), index=False, unique=False, nullable=False)
    DataOperation = relationship("DataOperation", back_populates="Contacts")