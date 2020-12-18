from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, Unicode, DateTime
from sqlalchemy.orm import relationship

from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity


class PythonDataIntegrationJob(Entity, IocManager.Base):
    __tablename__ = "PythonDataIntegrationJob"
    __table_args__ = {"schema": "Integration"}
    PythonDataIntegrationId = Column(Integer, ForeignKey('Integration.PythonDataIntegration.Id'))
    ApSchedulerJobId = Column(Integer, ForeignKey('Aps.ApSchedulerJob.Id'))
    StartDate = Column(DateTime, index=False, unique=False, nullable=False, default=datetime.now)
    EndDate = Column(DateTime, index=False, unique=False, nullable=True)
    Cron = Column(String(100), index=False, unique=False, nullable=True)
    PythonDataIntegration = relationship("PythonDataIntegration", back_populates="Jobs")
    def __init__(self,
                 StartDate: datetime = None,
                 EndDate: datetime = None,
                 Cron: str = None,
                 PythonDataIntegrationId:int=None,
                 ApSchedulerJobId: int = None,
                 PythonDataIntegration=None,
                 ApSchedulerJob=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.StartDate: datetime = StartDate
        self.EndDate: datetime = EndDate
        self.Cron: int = Cron
        self.PythonDataIntegrationId: int = PythonDataIntegrationId
        self.ApSchedulerJobId: int = ApSchedulerJobId
        self.PythonDataIntegration = PythonDataIntegration
        self.ApSchedulerJob = ApSchedulerJob
