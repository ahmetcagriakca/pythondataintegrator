from typing import List

from pdip.data import EntityBase

from pdi.domain.base.aps.ApSchedulerJobEventBase import ApSchedulerJobEventBase
from pdi.domain.base.operation.DataOperationJobBase import DataOperationJobBase


class ApSchedulerJobBase(EntityBase):
    def __init__(self,
                 JobId: str = None,
                 NextRunTime: float = None,
                 FuncRef=None,
                 JobEvents: List[ApSchedulerJobEventBase] = [],
                 DataOperationJobs: List[DataOperationJobBase] = [],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.JobId: int = JobId
        self.NextRunTime: str = NextRunTime
        self.FuncRef = FuncRef
        self.JobEvents = JobEvents
        self.DataOperationJobs = DataOperationJobs