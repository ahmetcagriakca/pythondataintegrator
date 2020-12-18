from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity


class PythonDataIntegrationExecutionJob(Entity, IocManager.Base):
    __tablename__ = "PythonDataIntegrationExecutionJob"
    __table_args__ = {"schema": "Integration"}
    PythonDataIntegrationId = Column(Integer, ForeignKey('Integration.PythonDataIntegration.Id'))
    ExecutionProcedure = Column(String(1000), index=False, unique=False, nullable=True)
    IsPre = Column(Boolean, index=False, unique=False, nullable=True)
    IsPost = Column(Boolean, index=False, unique=False, nullable=True)
    PythonDataIntegration = relationship("PythonDataIntegration", back_populates="ExecutionJobs")

    def __init__(self,
                 ExecutionProcedure: str = None,
                 IsPre: bool = None,
                 IsPost: bool = None,
                 PythonDataIntegration=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ExecutionProcedure: str = ExecutionProcedure
        self.IsPre: str = IsPre
        self.IsPost: str = IsPost
        self.PythonDataIntegration = PythonDataIntegration
