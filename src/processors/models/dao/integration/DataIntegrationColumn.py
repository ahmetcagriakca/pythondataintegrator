from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity


class DataIntegrationColumn(Entity, IocManager.Base):
    __tablename__ = "DataIntegrationColumn"
    __table_args__ = {"schema": "Integration"}
    DataIntegrationId = Column(Integer, ForeignKey('Integration.DataIntegration.Id'))
    ResourceType = Column(String(100), index=False, unique=False, nullable=True)
    SourceColumnName = Column(String(100), index=False, unique=False, nullable=True)
    TargetColumnName = Column(String(100), index=False, unique=False, nullable=True)
    DataIntegration = relationship("DataIntegration", back_populates="Columns")

    def __init__(self,
                 ResourceType: str = None,
                 SourceColumnName: str = None,
                 TargetColumnName: str = None,
                 DataIntegration=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ResourceType: str = ResourceType
        self.SourceColumnName: str = SourceColumnName
        self.TargetColumnName: str = TargetColumnName
        self.DataIntegration = DataIntegration
