

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity


class DataOperationExecutionProcess(Entity, IocManager.Base):
    __tablename__ = "DataOperationExecutionProcess"
    __table_args__ = {"schema": "Operation"}
    DataOperationExecutionId = Column(Integer, ForeignKey('Operation.DataOperationExecution.Id'))
    StatusId = Column(Integer, ForeignKey('Operation.DataOperationExecutionProcessStatus.Id'))
    ProcessId = Column(Integer, index=False, unique=False, nullable=True)
    SubLimit = Column(Integer, index=False, unique=False, nullable=False)
    TopLimit = Column(Integer, index=False, unique=False, nullable=False)
    ElapsedTime = Column(Float(precision=2), index=False, unique=False, nullable=True)
    Status = relationship("DataOperationExecutionProcessStatus", back_populates="DataOperationExecutionProcesses")
    DataOperationExecution = relationship("DataOperationExecution", back_populates="Processes")

    def __init__(self,
                 DataOperationExecutionId: int = None,
                 StatusId: int = None,
                 SubLimit: int = None,
                 TopLimit: int = None,
                 Status = None,
                 DataOperationExecution: bool = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataOperationExecutionId: int = DataOperationExecutionId
        self.StatusId: int = StatusId
        self.SubLimit: int = SubLimit
        self.TopLimit: int = TopLimit
        self.Status = Status
        self.DataOperationExecution = DataOperationExecution
