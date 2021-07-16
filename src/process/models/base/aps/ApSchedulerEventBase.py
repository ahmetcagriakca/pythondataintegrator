from typing import List

from models.base.aps.ApSchedulerJobEventBase import ApSchedulerJobEventBase
from models.base.EntityBase import EntityBase
from infrastructure.json.BaseConverter import BaseConverter


@BaseConverter.register
class ApSchedulerEventBase(EntityBase):
    def __init__(self,
                 Code: int = None,
                 Name: str = None,
                 Description: str = None,
                 Class: str = None,
                 JobEvents: List[ApSchedulerJobEventBase] = [],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Code: int = Code
        self.Name: str = Name
        self.Description: str = Description
        self.Class: str = Class
        self.JobEvents = JobEvents
