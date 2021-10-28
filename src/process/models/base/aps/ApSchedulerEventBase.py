from typing import List

from pdip.data import EntityBase

from .ApSchedulerJobEventBase import ApSchedulerJobEventBase


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
