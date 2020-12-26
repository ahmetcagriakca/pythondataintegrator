from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity


class DataIntegrationExecutionJob(Entity, IocManager.Base):
    __tablename__ = "DataIntegrationExecutionJob"
    __table_args__ = {"schema": "Integration"}
    DataIntegrationId = Column(Integer, ForeignKey('Integration.DataIntegration.Id'))
    ExecutionProcedure = Column(String(1000), index=False, unique=False, nullable=True)
    IsPre = Column(Boolean, index=False, unique=False, nullable=True)
    IsPost = Column(Boolean, index=False, unique=False, nullable=True)
    DataIntegration = relationship("DataIntegration", back_populates="ExecutionJobs")

    def __init__(self,
                 ExecutionProcedure: str = None,
                 IsPre: bool = None,
                 IsPost: bool = None,
                 DataIntegration=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ExecutionProcedure: str = ExecutionProcedure
        self.IsPre: str = IsPre
        self.IsPost: str = IsPost
        self.DataIntegration = DataIntegration
