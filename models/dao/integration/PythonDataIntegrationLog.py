from sqlalchemy import Column, String, Integer, DateTime
from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity


class PythonDataIntegrationLog(Entity, IocManager.Base):
    __tablename__ = "PythonDataIntegrationLog"
    __table_args__ = {"schema": "Integration"}
    TypeId = Column(Integer, index=True, unique=False, nullable=False)
    Content = Column(String(4000), index=False, unique=False, nullable=True)
    LogDatetime = Column(DateTime, index=False, unique=False, nullable=True)
    JobId = Column(Integer, index=True, unique=False, nullable=True)

    def __init__(self,
                 TypeId: str = None,
                 Content: str = None,
                 LogDatetime: DateTime = None,
                 JobId: int = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TypeId = TypeId
        self.Content = Content
        self.LogDatetime = LogDatetime
        self.JobId = JobId
