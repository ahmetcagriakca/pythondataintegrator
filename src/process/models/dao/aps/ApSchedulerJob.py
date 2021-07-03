from typing import List
from sqlalchemy.orm import relationship

from models.base.aps.ApSchedulerJobBase import ApSchedulerJobBase
from models.dao.aps.ApSchedulerJobEvent import ApSchedulerJobEvent
from models.dao.Entity import Entity
from sqlalchemy import Column, String, TEXT, Unicode, DateTime
from IocManager import IocManager
from models.dao.operation.DataOperationJob import DataOperationJob


class ApSchedulerJob(ApSchedulerJobBase,Entity, IocManager.Base):
    __tablename__ = "ApSchedulerJob"
    __table_args__ = {"schema": "Aps"}

    JobId = Column(Unicode(191, _warn_on_bytestring=False))
    NextRunTime = Column(DateTime)
    FuncRef = Column(String(500), nullable=False)
    JobEvents: List[ApSchedulerJobEvent] = relationship("ApSchedulerJobEvent", back_populates="ApSchedulerJob")
    DataOperationJobs: List[DataOperationJob] = relationship("DataOperationJob", back_populates="ApSchedulerJob")
