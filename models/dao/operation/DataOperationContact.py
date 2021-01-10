from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity


class DataOperationContact(Entity, IocManager.Base):
    __tablename__ = "DataOperationContact"
    __table_args__ = {"schema": "Operation"}
    DataOperationId = Column(Integer, ForeignKey('Operation.DataOperation.Id'))
    Email = Column(String(250), index=False, unique=False, nullable=False)
    DataOperation = relationship("DataOperation", back_populates="Contacts")

    def __init__(self,
                 DataOperationId: int = None,
                 Email: str = None,
                 DataOperation = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataOperationId: int = DataOperationId
        self.Email: int = Email
        self.DataOperation = DataOperation
