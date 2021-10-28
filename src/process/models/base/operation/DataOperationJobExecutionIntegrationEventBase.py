from datetime import datetime

from pdip.data import EntityBase


class DataOperationJobExecutionIntegrationEventBase(EntityBase):

    def __init__(self,
                 DataOperationJobExecutionIntegrationId: int = None,
                 EventId: int = None,
                 EventDate: datetime = None,
                 AffectedRowCount: int = None,
                 Event: any = None,
                 DataOperationJobExecutionIntegration: any = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataOperationJobExecutionIntegrationId: int = DataOperationJobExecutionIntegrationId
        self.EventId: int = EventId
        self.EventDate: datetime = EventDate
        self.AffectedRowCount: int = AffectedRowCount
        self.Event = Event
        self.DataOperationJobExecutionIntegration = DataOperationJobExecutionIntegration
