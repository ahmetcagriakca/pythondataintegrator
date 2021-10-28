from datetime import datetime
from typing import List

from pdip.data import EntityBase

from models.base.operation.DataOperationJobExecutionIntegrationEventBase import \
    DataOperationJobExecutionIntegrationEventBase


class DataOperationJobExecutionIntegrationBase(EntityBase):

    def __init__(self,
                 DataOperationJobExecutionId: int = None,
                 DataOperationIntegrationId: int = None,
                 StatusId: int = None,
                 StartDate: datetime = None,
                 EndDate: datetime = None,
                 Limit: int = None,
                 ProcessCount: int = None,
                 SourceDataCount: int = None,
                 Log: str = None,
                 DataOperationIntegration: any = None,
                 DataOperationJobExecution: any = None,
                 DataOperationJobExecutionIntegrationEvents: List[DataOperationJobExecutionIntegrationEventBase] = [],
                 Status: any = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataOperationJobExecutionIntegrationEvents = DataOperationJobExecutionIntegrationEvents
        self.DataOperationJobExecutionId: int = DataOperationJobExecutionId
        self.DataOperationIntegrationId: int = DataOperationIntegrationId
        self.StatusId: int = StatusId
        self.StartDate: datetime = StartDate
        self.EndDate: datetime = EndDate
        self.Limit: int = Limit
        self.ProcessCount: int = ProcessCount
        self.SourceDataCount: int = SourceDataCount
        self.Log: str = Log
        self.DataOperationIntegration: any = DataOperationIntegration
        self.DataOperationJobExecution: any = DataOperationJobExecution
        self.Status: any = Status
