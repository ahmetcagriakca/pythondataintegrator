from datetime import datetime

from pdip.data import EntityBase


class DataOperationJobExecutionBase(EntityBase):

    def __init__(self,
                 DefinitionId: int = None,
                 DataOperationId: int = None,
                 DataOperationJobId: int = None,
                 StatusId: int = None,
                 StartDate: datetime = None,
                 EndDate: datetime = None,
                 Status=None,
                 Definition=None,
                 DataOperationJob=None,
                 DataOperationJobExecutionEvents=[],
                 DataOperationJobExecutionIntegrations=[],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataOperationJobExecutionIntegrations = DataOperationJobExecutionIntegrations
        self.DataOperationJobExecutionEvents = DataOperationJobExecutionEvents
        self.DefinitionId: int = DefinitionId
        self.DataOperationId: int = DataOperationId
        self.DataOperationJobId: int = DataOperationJobId
        self.StatusId: int = StatusId
        self.StartDate: datetime = StartDate
        self.EndDate: datetime = EndDate
        self.DataOperationJob = DataOperationJob
        self.Status = Status
        self.Definition = Definition
