from datetime import datetime
from typing import List

from pdip.data.domain import EntityBase

from src.domain.base.operation.DataOperationJobExecutionBase import DataOperationJobExecutionBase


class DataOperationJobBase(EntityBase):

    def __init__(self,
                 DataOperationId: int = None,
                 ApSchedulerJobId: int = None,
                 StartDate: datetime = None,
                 EndDate: datetime = None,
                 Cron: str = None,
                 DataOperation=None,
                 ApSchedulerJob=None,
                 DataOperationJobExecutions: List[DataOperationJobExecutionBase] = [],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataOperationJobExecutions = DataOperationJobExecutions
        self.DataOperationId: int = DataOperationId
        self.ApSchedulerJobId: int = ApSchedulerJobId
        self.StartDate: datetime = StartDate
        self.EndDate: datetime = EndDate
        self.Cron: int = Cron
        self.DataOperation = DataOperation
        self.ApSchedulerJob = ApSchedulerJob
