from typing import List
from models.dao.aps.ApSchedulerJobEvent import ApSchedulerJobEvent
from pdip.data import Entity
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from pdip.dependency.container import DependencyContainer


class ApSchedulerEvent(Entity, DependencyContainer.Base):
    __tablename__ = "ApSchedulerEvent"
    __table_args__ = {"schema": "Aps"}

    Code = Column(Integer, nullable=False)
    Name = Column(String(255), nullable=False)
    Description = Column(String(1000), nullable=False)
    Class = Column(String(255), nullable=False)
    JobEvents: List[ApSchedulerJobEvent] = relationship("ApSchedulerJobEvent", back_populates="ApSchedulerEvent")

    def __init__(self,
                 Code: int = None,
                 Name: str = None,
                 Description: str = None,
                 Class: str = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Code: int = Code
        self.Name: str = Name
        self.Description: str = Description
        self.Class: str = Class
