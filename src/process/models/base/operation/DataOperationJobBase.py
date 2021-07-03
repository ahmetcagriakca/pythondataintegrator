from datetime import datetime
from typing import List
from models.base.EntityBase import EntityBase
from models.base.operation.DataOperationJobExecutionBase import DataOperationJobExecutionBase
from infrastructor.json.BaseConverter import BaseConverter


@BaseConverter.register
class DataOperationJobBase(EntityBase):

    def __init__(self,
                 DataOperationId: int = None,
                 ApSchedulerJobId: int = None,
                 StartDate: datetime = None,
                 EndDate: datetime = None,
                 Cron: str = None,
                 DataOperation=None,
                 ApSchedulerJob=None,
                 DataOperationJobExecutions: List[DataOperationJobExecutionBase]=[],
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
